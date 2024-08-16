import warnings

# Suppress specific Pydantic warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic._internal._config")

import time
from retrying import retry
import cohere
import argparse
from config import COHERE_API_KEY
from colorama import Fore, Style, init
from urllib.parse import quote_plus

# Initialize colorama
init(autoreset=True)

# Initialize the Cohere API client using the provided API key
co = cohere.Client(api_key=COHERE_API_KEY)

def print_step(step_text, color=Fore.CYAN):
    print(f"{color}[*] {step_text}{Style.RESET_ALL}")

def print_warning(step_text):
    print(f"{Fore.YELLOW}[!] {step_text}{Style.RESET_ALL}")

def print_error(step_text):
    print(f"{Fore.RED}[X] {step_text}{Style.RESET_ALL}")

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_blog_content(prompt, max_words=None, min_words=None, language='English'):
    # Create a detailed prompt for the Cohere API
    engineered_prompt = f"""
    I want you to act as a professional content writer with expertise in SEO and blog writing. Create a comprehensive 2000-word blog article in {language} on the topic provided. The article should include:
    1. An outline with at least 15 headings and subheadings.
    2. Detailed, engaging content under each heading.
    3. SEO-optimized keywords and a meta description.

    For each section of the article, suggest relevant images by providing image descriptions or URLs suitable for that section. Make sure to incorporate these images in the Markdown format of the article.

    Use conversational and human-like writing style, ensuring the content is unique, informative, and engaging. End with a conclusion paragraph and 5 unique FAQs after the conclusion. Bold the title and all headings.

    Here is the topic: "{prompt}"
    """

    # Add max_words and min_words to the prompt if specified
    if max_words:
        engineered_prompt += f"\nMaximum Words: {max_words}"
    if min_words:
        engineered_prompt += f"\nMinimum Words: {min_words}"

    # Call the Cohere API to generate the blog content
    stream = co.chat_stream(
        model='command-r-plus',  # Specify the model to be used for generation
        message=engineered_prompt,  # Pass the engineered prompt to the API
        temperature=0.3,  # Set the temperature for creativity
        chat_history=[],  # No prior chat history
        prompt_truncation='AUTO'  # Handle prompt truncation automatically
    )

    # Accumulate the generated blog content
    blog_content = ""
    for event in stream:
        if event.event_type == "text-generation":
            blog_content += event.text

    return blog_content

def generate_image_topics(headline):
    # Generate image topics based on the headline
    topics_prompt = f"""
    Generate a list of keywords or topics for images based on the following headline. Provide the topics separated by commas. Here is the headline:
    {headline}
    """
    try:
        response = co.generate(
            model='command-r-plus',
            prompt=topics_prompt,
            max_tokens=50,
            temperature=0.5,
        )
        topics = response.generations[0].text.strip()
    except Exception as e:
        print_error(f"Failed to generate image topics: {e}")
        topics = headline  # Fallback to headline as topics if AI fails

    return topics

def generate_image_url(meta_keywords):
    # Extract the first two keywords from meta_keywords
    meta_keywords_list = [keyword.strip() for keyword in meta_keywords.split(',')]
    first_two_keywords = ','.join(meta_keywords_list[:2])  # Get the first two keywords
    encoded_keywords = quote_plus(first_two_keywords)  # URL-encode the keywords
    
    # Generate the URL with only the first two keywords
    return f"https://loremflickr.com/800/600/{encoded_keywords.replace('%2C', ',')}"



def generate_meta_keywords(content):
    # Generate SEO meta keywords from the content
    keywords_prompt = f"""
    Generate a list of SEO keywords relevant to the following blog content. The keywords should be separated by commas and should be highly relevant to the content. Here is the content:
    {content}
    """
    try:
        response = co.generate(
            model='command-r-plus',
            prompt=keywords_prompt,
            max_tokens=50,
            temperature=0.5,
        )
        keywords = response.generations[0].text.strip()
    except Exception as e:
        print_error(f"Failed to generate keywords: {e}")
        keywords = "default, keywords, here"

    return keywords

def github_readme_font(content):
    # Generate GitHub README specific font formatting
    readme_prompt = f"""
    Convert the following blog content into GitHub README style formatting. The content should be formatted in Markdown suitable for a GitHub README file. Here is the content:
    {content}
    """
    try:
        response = co.generate(
            model='command-r-plus',
            prompt=readme_prompt,
            max_tokens=1000,
            temperature=0.5,
        )
        readme_content = response.generations[0].text.strip()
    except Exception as e:
        print_error(f"Failed to generate README formatting: {e}")
        readme_content = content

    return readme_content


    try:
        # Log step: Starting blog content generation
        print_step(f"Generating blog content for the topic: {prompt}")

        # Fetch blog content with retry
        blog_content = fetch_blog_content(prompt, max_words, min_words, language)

        # Log step: Cleaning up blog content
        print_step("Cleaning up the generated blog content...")
        
        # Clean up the blog content by removing unwanted prefixes and adjusting markdown formatting
        blog_content = blog_content.replace("## Outline:", "").strip()
        blog_content = blog_content.replace("## Article:", "").strip()
        blog_content = blog_content.replace("#### H4:", "####")
        blog_content = blog_content.replace("### H3:", "###")
        blog_content = blog_content.replace("## H2:", "##")
        blog_content = blog_content.replace("# H1:", "#")

        # Ensure the first line is a top-level heading
        if not blog_content.startswith("# "):
            blog_content = f"# {prompt}\n\n" + blog_content

        # Remove trailing punctuation from headings
        lines = blog_content.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith('#'):
                lines[i] = lines[i].rstrip(':')

        # Generate meta keywords
        meta_keywords = generate_meta_keywords(blog_content)

        # Replace section headings with image placeholders from loremflickr.com
        for i, line in enumerate(lines):
            if line.startswith('# '):  # Heading line
                section_title = line[2:]  # Remove the '# ' prefix
                image_topics = generate_image_topics(section_title)
                image_url = generate_image_url(image_topics, meta_keywords)
                lines[i] = f'{line}\n![Image]({image_url})'

        # Join the lines to form the final Markdown content
        markdown_content = '\n'.join(lines)

        # Generate SEO meta description
        description_prompt = f"Generate a brief and relevant meta description for this content. Just give the meta description that is SEO friendly and relevant, don't give any extra words, or any prefix or suffix. Here is the content:\n{markdown_content}"
        try:
            description_response = co.generate(
                model='command-r-plus',
                prompt=description_prompt,
                max_tokens=50,
                temperature=0.5,
            )
            description = description_response.generations[0].text.strip()
        except Exception as e:
            print_error(f"Failed to generate description: {e}")
            description = "Default SEO description"

        # Convert to GitHub README style if requested
        if output_format.lower() == 'github':
            markdown_content = github_readme_font(markdown_content)

        # Log step: Creating the output file
        print_step(f"Creating the output file in {output_format} format...")

        # Generate the output file based on the requested format
        try:
            if output_format.lower() == 'html':
                output_file = f"{file_name or prompt}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('<!DOCTYPE html>\n')
                    f.write('<html lang="en">\n<head>\n')
                    f.write(f'<meta charset="UTF-8">\n')
                    f.write(f'<meta name="description" content="{description}">\n')
                    f.write(f'<meta name="keywords" content="{meta_keywords}">\n')
                    f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
                    f.write(f'<title>{prompt}</title>\n')
                    f.write('</head>\n<body>\n')
                    f.write('<h1>' + prompt + '</h1>\n')
                    f.write('<markdown>\n')
                    f.write(markdown_content)
                    f.write('\n</markdown>\n')
                    f.write('<script src="https://cdn.jsdelivr.net/gh/OCEANOFANYTHINGOFFICIAL/mdonhtml.js/scripts/mdonhtml.min.js"></script>\n')
                    f.write('\n</body>\n</html>')
            elif output_format.lower() in ['md', 'github']:
                output_file = f"{file_name or prompt}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
            else:
                print_error(f"Invalid output format: {output_format}")
        except Exception as e:
            print_error(f"Failed to save the blog content: {e}")

    except Exception as e:
        print_error(f"Failed to generate the blog: {e}")

def generate_blog(prompt, max_words=None, min_words=None, output_format='HTML', file_name=None, language='English'):
    try:
        # Log step: Starting blog content generation
        print_step(f"Generating blog content for the topic: {prompt}")

        # Fetch blog content with retry
        blog_content = fetch_blog_content(prompt, max_words, min_words, language)

        # Log step: Cleaning up blog content
        print_step("Cleaning up the generated blog content...")
        
        # Clean up the blog content by removing unwanted prefixes and adjusting markdown formatting
        blog_content = blog_content.replace("## Outline:", "").strip()
        blog_content = blog_content.replace("## Article:", "").strip()
        blog_content = blog_content.replace("#### H4:", "####")
        blog_content = blog_content.replace("### H3:", "###")
        blog_content = blog_content.replace("## H2:", "##")
        blog_content = blog_content.replace("# H1:", "#")

        # Ensure the first line is a top-level heading
        if not blog_content.startswith("# "):
            blog_content = f"# {prompt}\n\n" + blog_content

        # Remove trailing punctuation from headings
        lines = blog_content.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith('#'):
                lines[i] = lines[i].rstrip(':')

        # Replace section headings with image placeholders from loremflickr.com
        for i, line in enumerate(lines):
            if line.startswith('# '):  # Heading line
                section_title = line[2:]  # Remove the '# ' prefix
                meta_keywords = generate_meta_keywords(blog_content)
                image_url = generate_image_url(meta_keywords)
                lines[i] = f'{line}\n![Image]({image_url})'

        # Join the lines to form the final Markdown content
        markdown_content = '\n'.join(lines)

        # Generate SEO meta description
        description_prompt = f"Generate a brief and relevant meta description for this content. Just give the meta description that is SEO friendly and relevant, don't give any extra words, or any prefix or suffix. Here is the content:\n{markdown_content}"
        try:
            description_response = co.generate(
                model='command-r-plus',
                prompt=description_prompt,
                max_tokens=50,
                temperature=0.5,
            )
            description = description_response.generations[0].text.strip()
        except Exception as e:
            print_error(f"Failed to generate description: {e}")
            description = "Default SEO description"

        # Generate meta keywords
        meta_keywords = generate_meta_keywords(markdown_content)

        # Convert to GitHub README style if requested
        if output_format.lower() == 'github':
            markdown_content = github_readme_font(markdown_content)

        # Log step: Creating the output file
        print_step(f"Creating the output file in {output_format} format...")

        # Generate the output file based on the requested format
        try:
            if output_format.lower() == 'html':
                output_file = f"{file_name or prompt}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('<!DOCTYPE html>\n')
                    f.write('<html lang="en">\n<head>\n')
                    f.write(f'<meta charset="UTF-8">\n')
                    f.write(f'<meta name="description" content="{description}">\n')
                    f.write(f'<meta name="keywords" content="{meta_keywords}">\n')
                    f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
                    f.write(f'<title>{prompt}</title>\n')
                    f.write('</head>\n<body>\n')
                    f.write('<h1>' + prompt + '</h1>\n')
                    f.write('<markdown>\n')
                    f.write(markdown_content)
                    f.write('\n</markdown>\n')
                    f.write('<script src="https://cdn.jsdelivr.net/gh/OCEANOFANYTHINGOFFICIAL/mdonhtml.js/scripts/mdonhtml.min.js"></script>\n')
                    f.write('\n</body>\n</html>')
            elif output_format.lower() in ['md', 'github']:
                output_file = f"{file_name or prompt}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
            else:
                print_error(f"Invalid output format: {output_format}")
        except Exception as e:
            print_error(f"Failed to save the blog content: {e}")

    except Exception as e:
        print_error(f"Failed to generate the blog: {e}")


def main():
    # Set up argument parser for command-line interface
    parser = argparse.ArgumentParser(description='AI Blog Generator')
    parser.add_argument('topic', type=str, help='Topic of the blog')  # Required argument for blog topic
    parser.add_argument('-mw', '--max_words', type=int, help='Maximum number of words')  # Optional max words argument
    parser.add_argument('-mnw', '--min_words', type=int, help='Minimum number of words')  # Optional min words argument
    parser.add_argument('-of', '--output_format', type=str, choices=['HTML', 'Markdown', 'md', 'github'], default='HTML', help='Output format (HTML, Markdown, md, GitHub)')  # Optional output format argument
    parser.add_argument('-fn', '--file_name', type=str, help='Output file name')  # Optional file name argument
    parser.add_argument('-l', '--language', type=str, default='English', help='Language of the article')  # Optional language argument

    args = parser.parse_args()

    # Ensure that at least one of max_words or min_words is provided
    if not args.max_words and not args.min_words:
        parser.error('At least one of --max_words or --min_words is required.')

    # Generate the blog based on parsed arguments
    generate_blog(args.topic, args.max_words, args.min_words, args.output_format, args.file_name, args.language)

if __name__ == '__main__':
    main()
