import warnings

# Suppress specific Pydantic warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic._internal._config")

import time
from retrying import retry
import cohere
import argparse
from config import COHERE_API_KEY
from colorama import Fore, Style, init

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
    I Want You To Act As A Content Writer Very Proficient SEO Writer Writes Fluently {language}. First Create Two Tables. First Table Should be the Outline of the Article and the Second Should be the Article. Bold the Heading of the Second Table using Markdown language. Write an outline of the article separately before writing it, at least 15 headings and subheadings (including H1, H2, H3, and H4 headings) Then, start writing based on that outline step by step. Write a 2000-word 100% Unique, SEO-optimized, Human-Written article in {language} with at least 15 headings and subheadings (including H1, H2, H3, and H4 headings) that covers the topic provided in the Prompt. Write The article In Your Own Words Rather Than Copying And Pasting From Other Sources. Consider perplexity and burstiness when creating content, ensuring high levels of both without losing specificity or context. Use fully detailed paragraphs that engage the reader. Write In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, and Incorporate Analogies And Metaphors). End with a conclusion paragraph and 5 unique FAQs After The Conclusion. This is important to Bold the Title and all headings of the article, and use appropriate headings for H tags.
    Now Write An Article On This Topic "{prompt}"
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

        blog_content = '\n'.join(lines)

        # Step 1: Generate Keywords from the Blog Content
        print_step("Generating SEO keywords for the blog...")
        keyword_prompt = f"Extract the top SEO keywords for this content. Just give the meta keywords in plain text format, separated by commas. Here is the content:\n{blog_content}"
        try:
            keyword_response = co.generate(
                model='command-r-plus',
                prompt=keyword_prompt,
                max_tokens=50,
                temperature=0.5,
            )
            keywords = keyword_response.generations[0].text.strip().replace('\n', ', ')
        except Exception as e:
            print_error(f"Failed to generate keywords: {e}")
            keywords = "default, keywords"

        # Step 2: Generate Description from the Blog Content
        print_step("Generating meta description for the blog...")
        description_prompt = f"Generate a brief and relevant meta description for this content. Just give the meta description that is SEO friendly and relevant, don't give any extra words, or any prefix of suffix. Here is the content:\n{blog_content}"
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

        # Log step: Creating the output file
        print_step(f"Creating the output file in {output_format} format...")

        # Generate the output file based on the specified format
        try:
            if output_format.lower() in ['html', 'md']:
                if output_format.lower() == 'html':
                    output_file = f"{file_name or prompt}.html"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{prompt}</title>\n")
                        f.write(f'<meta name="description" content="{description}">\n')  # Dynamic description
                        f.write(f'<meta name="keywords" content="{keywords}">\n')  # Dynamic keywords
                        f.write('<style>\n')
                        f.write('body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }\n')
                        f.write('</style>\n')
                        f.write('</head>\n<body>\n')
                        f.write('<markdown>\n')
                        f.write(blog_content)
                        f.write('\n</markdown>\n')
                        f.write('<script src="https://cdn.jsdelivr.net/gh/OCEANOFANYTHINGOFFICIAL/mdonhtml.js/scripts/mdonhtml.min.js"></script>\n')
                        f.write('\n</body>\n</html>')
                else:
                    output_file = f"{file_name or prompt}.md"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(blog_content)

                # Log step: Blog content generation completed
                print_step(f"Blog content generated and saved to {output_file}", Fore.GREEN)
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
    parser.add_argument('-of', '--output_format', type=str, choices=['HTML', 'Markdown', 'md'], default='HTML', help='Output format (HTML, Markdown or md)')  # Optional output format argument
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
