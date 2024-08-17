import warnings

# Suppress specific Pydantic warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic._internal._config")


import random
from retrying import retry
import cohere
import argparse
from config import COHERE_API_KEY
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Initialize the Cohere API client using the provided API key
co = cohere.Client(api_key=COHERE_API_KEY)

def print_step(step_text):
    """
    Print a step message with Cyan color.
    """
    print(f"{Fore.CYAN}[*] {step_text}{Style.RESET_ALL}")

def print_success(step_text):
    """
    Print a success message with Green color.
    """
    print(f"{Fore.GREEN}[+] {step_text}{Style.RESET_ALL}")

def print_warning(step_text):
    """
    Print a warning message with Yellow color.
    """
    print(f"{Fore.YELLOW}[!] {step_text}{Style.RESET_ALL}")

def print_error(step_text):
    """
    Print an error message with Red color.
    """
    print(f"{Fore.RED}[X] {step_text}{Style.RESET_ALL}")

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_blog_content(prompt, max_words=None, min_words=None, language='English'):
    """
    Generate a blog article based on the provided prompt using the Cohere API.
    Args:
        prompt (str): The topic or prompt for the blog article.
        max_words (int): The maximum number of words for the blog article.
        min_words (int): The minimum number of words for the blog article.
        language (str): The language for the blog article (default is English).
    Returns:
        str: The generated blog content based on the prompt
    """
    
    # Create a detailed prompt for the Cohere API
    engineered_prompt = f"""
    I want you to act as a professional content writer with expertise in SEO and blog writing. Create a comprehensive 2000-word blog article in {language} on the topic provided. The article should include:
    1. An outline with at least 15 headings and subheadings.
    2. Detailed, engaging content under each heading.
    3. SEO-optimized keywords and a meta description.

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
    """
    Generate image topics based on the provided headline using the Cohere API.
    Args:
        headline (str): The headline or title for the blog article.
    Returns:
        str: The generated image topics based on the headline
    """
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
    """
    Generate a random image URL based on the provided meta keywords.
    Args:
        meta_keywords (str): The meta keywords for the blog article.
    Returns:
        str: A random image URL based on the meta keywords
    """
    
    # Extract keywords from the meta_keywords
    keywords_list = [keyword.strip() for keyword in meta_keywords.split(',')]
    
    # Choose a single random keyword from the list
    random_keyword = random.choice(keywords_list) if keywords_list else 'default'
    
    # Get the first word from the random keyword
    random_keyword = random_keyword.split()[0]
    
    # Generate the URL with the selected keyword
    return f"https://loremflickr.com/800/600/{random_keyword.replace(' ', ',')}"

def generate_meta_keywords(content):
    """
    Generate SEO meta keywords based on the provided content using the Cohere API.
    Args:
        content (str): The blog content for generating meta keywords.
    Returns:
        str: The generated SEO meta keywords based on the content
    """
    
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
    """
    Convert the blog content into GitHub README specific font formatting.
    Args:
        content (str): The blog content to be converted.
    Returns:
        str: The blog content formatted in Markdown suitable for a GitHub README file.
    """
    
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
    """
    Generate a blog article based on the provided prompt and save it to an output file.
    Args:
        prompt (str): The topic or prompt for the blog article.
        max_words (int): The maximum number of words for the blog article.
        min_words (int): The minimum number of words for the blog article.
        output_format (str): The output format for the blog article (HTML, Markdown, GitHub).
        file_name (str): The name of the output file to be generated.
        language (str): The language for the blog article (default is English).
    Returns:
        None
    """
    
    try:
        # Log step: Starting blog content generation
        print_step(f"Generating blog content for the topic: {prompt}")

        # Fetch blog content with retry
        blog_content = fetch_blog_content(prompt, max_words, min_words, language)
        
        print_success("Blog content generated successfully!")

        # Log step: Cleaning up blog content
        print_step("Cleaning up the generated blog content...")
        
        # Clean up the blog content by removing unwanted prefixes and adjusting markdown formatting
        blog_content = blog_content.replace("## Outline:", "").strip()
        blog_content = blog_content.replace("## Article:", "").strip()
        blog_content = blog_content.replace("#### H4:", "####")
        blog_content = blog_content.replace("### H3:", "###")
        blog_content = blog_content.replace("## H2:", "##")
        blog_content = blog_content.replace("# H1:", "#")
        
        print_success("Blog content cleaned up successfully!")

        # Ensure the first line is a top-level heading
        if not blog_content.startswith("# "):
            blog_content = f"# {prompt}\n\n" + blog_content

        # Remove trailing punctuation from headings
        lines = blog_content.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith('#'):
                lines[i] = lines[i].rstrip(':')

        # Replace section headings with image placeholders from loremflickr.com
        
        print_step("Generating & inserting image into the blog...")
        try:
            for i, line in enumerate(lines):
                if line.startswith('# '):  # Heading line
                    section_title = line[2:]  # Remove the '# ' prefix
                    meta_keywords = generate_meta_keywords(blog_content)
                    image_url = generate_image_url(meta_keywords)
                    lines[i] = f'{line}\n![Image]({image_url})'
            # Join the lines to form the final Markdown content
            markdown_content = '\n'.join(lines)
            print_success("Image generated and inserted successfully!")
        except Exception as e:
            print_error(f"Failed to generate and insert image: {e}")
            print_warning("Continuing without inserting images...")
            pass
        
        # Generate SEO meta description
        print_step(f"Generating SEO meta description for the blog: {prompt}")
        
        description_prompt = f"Generate a brief and relevant meta description for this content. Just give the meta description that is SEO friendly and relevant, don't give any extra words, or any prefix or suffix. Here is the content:\n{markdown_content}"
        try:
            description_response = co.generate(
                model='command-r-plus',
                prompt=description_prompt,
                max_tokens=50,
                temperature=0.5,
            )
            description = description_response.generations[0].text.strip()
            print_success("SEO meta description generated successfully!")
        except Exception as e:
            print_error(f"Failed to generate description: {e}")
            # Fallback to a default description which is the title of the blog separated by commas
            description = str(prompt)
            print_warning(f"Using the default description: {description}")

        # Generate meta keywords
        print_step(f"Generating meta keywords for the blog: {prompt}")
        
        try:
            meta_keywords = generate_meta_keywords(markdown_content)
            print_success("Meta keywords generated successfully!")
        except Exception as e:
            print_error(f"Failed to generate keywords: {e}")
            meta_keywords = ', '.join(prompt.split())
            print_warning(f"Using the blog title as meta keywords: {meta_keywords}")
        

        # Convert to GitHub README style if requested
        if output_format.lower() == 'github':
            try:
                markdown_content = github_readme_font(markdown_content)
                print_success("GitHub README formatting applied successfully!")
            except Exception as e:
                print_error(f"Failed to apply GitHub README formatting: {e}")
                print_warning("Continuing without GitHub README formatting...")
                pass

        # Log step: Creating the output file
        print_step(f"Creating the output file in {output_format} format...")

        # Generate the output file based on the requested format
        try:
            if output_format.lower() == 'html':
                output_file = f"{file_name or prompt}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    # Format the HTML content with the generated blog Markdown content.
                    # IMPORTANT: Dont change the format of the HTML content. It is required for perfect rendering and indentation of the blog content.
                    
                    f.write(f"""<!DOCTYPE html>
<html lang="en">

   <head>
      <meta charset="UTF-8">
      <meta name="description" content="{description}">
      <meta name="keywords"content="{meta_keywords}">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{prompt}</title>""")
                    f.write("""
      <style>
         body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
         }
      </style>""")
                    f.write(f"""
   </head>

   <body>
      <markdown>
         {markdown_content}
      </markdown>
      <script src="https://cdn.jsdelivr.net/gh/OCEANOFANYTHINGOFFICIAL/mdonhtml.js/scripts/mdonhtml.min.js"></script>
   </body>

</html>""")
                print_success(f"Blog content saved to: {output_file}")
            elif output_format.lower() in ['md', 'github']:
                try:
                    output_file = f"{file_name or prompt}.md"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    print_success(f"Blog content saved to: {output_file}")
                except Exception as e:
                    print_error(f"Failed to save the blog content: {e}")
            else:
                print_error(f"Invalid output format: {output_format}")
        except Exception as e:
            print_error(f"Failed to save the blog content: {e}")
    except Exception as e:
        print_error(f"Failed to generate the blog: {e}")


def main():
    """
    Main function to parse command-line arguments and generate a blog article.
    """
    
    # Set up argument parser for command-line interface
    parser = argparse.ArgumentParser(description='AI Blog Generator')
    parser.add_argument('topic', type=str, help='Topic of the blog')  # Required argument for blog topic
    parser.add_argument('-mw', '--max_words', type=int, help='Maximum number of words')  # Optional max words argument
    parser.add_argument('-mnw', '--min_words', type=int, help='Minimum number of words')  # Optional min words argument
    parser.add_argument('-of', '--output_format', type=str, choices=['HTML', 'Markdown', 'md', 'github'], default='HTML', help='Output format (HTML, Markdown, md, GitHub)')  # Optional output format argument
    parser.add_argument('-fn', '--file_name', type=str, help='Output file name')  # Optional file name argument
    parser.add_argument('-l', '--language', type=str, default='English', help='Language of the article')  # Optional language argument
    parser.add_argument('-gr', '--github_readme', action='store_true', help='Convert content to GitHub README format')  # Small flag for GitHub README formatting

    args = parser.parse_args()

    # Ensure that at least one of max_words or min_words is provided
    if not args.max_words and not args.min_words:
        parser.error('At least one of --max_words or --min_words is required.')

    # Check if the GitHub README formatting flag is set
    if args.github_readme:
        args.output_format = 'github'

    # Generate the blog based on parsed arguments
    generate_blog(args.topic, args.max_words, args.min_words, args.output_format, args.file_name, args.language)

if __name__ == '__main__':
    main()
