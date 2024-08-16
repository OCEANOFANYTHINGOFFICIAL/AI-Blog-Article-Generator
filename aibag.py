import cohere
import argparse
from config import COHERE_API_KEY

# Initialize the Cohere API client using the provided API key
co = cohere.Client(api_key=COHERE_API_KEY)

def generate_blog(prompt, max_words=None, min_words=None, output_format='HTML', file_name=None, language='English'):
    # Create a detailed prompt for the Cohere API
    engineered_prompt = f"""
    I Want You To Act As A Content Writer Very Proficient SEO Writer Writes Fluently {language}. First Create Two Tables. First Table Should be the Outline of the Article and the Second Should be the Article. Bold the Heading of the Second Table using Markdown language. Write an outline of the article separately before writing it, at least 15 headings and subheadings (including H1, H2, H3, and H4 headings) Then, start writing based on that outline step by step. Write a 2000-word 100% Unique, SEO-optimized, Human-Written article in {language} with at least 15 headings and subheadings (including H1, H2, H3, and H4 headings) that covers the topic provided in the Prompt. Write The article In Your Own Words Rather Than Copying And Pasting From Other Sources. Consider perplexity and burstiness when creating content, ensuring high levels of both without losing specificity or context. Use fully detailed paragraphs that engage the reader. Write In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, and Incorporate Analogies And Metaphors). End with a conclusion paragraph and 5 unique FAQs After The Conclusion. This is important to Bold the Title and all headings of the article, and use appropriate headings for H tags.
    Now Write An Article On This Topic "{prompt}"
    """

    # Notify the user that the blog content generation is in progress
    print("Generating blog content...")

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
    keyword_prompt = f"Extract the top SEO keywords for this content:\n{blog_content}"
    keyword_response = co.generate(
        model='command-xlarge-20220609',
        prompt=keyword_prompt,
        max_tokens=50,
        temperature=0.5,
    )
    keywords = keyword_response.generations[0].text.strip().replace('\n', ', ')

    # Generate the output file based on the specified format
    if output_format.lower() == 'html':
        output_file = f"{file_name or prompt}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{prompt}</title>\n")
            f.write(f'<meta name="description" content="SEO optimized blog">\n')  # Placeholder for description
            f.write(f'<meta name="keywords" content="{keywords}">\n')  # Updated keywords meta tag
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

    # Notify the user that the blog content has been generated and saved
    print(f"Blog content generated and saved to {output_file}")

    # Create a detailed prompt for the Cohere API
    engineered_prompt = f"""
    I Want You To Act As A Content Writer Very Proficient SEO Writer Writes Fluently {language}. First Create Two Tables. First Table Should be the Outline of the Article and the Second Should be the Article. Bold the Heading of the Second Table using Markdown language. Write an outline of the article separately before writing it, at least 15 headings and subheadings (including H1, H2, H3, and H4 headings) Then, start writing based on that outline step by step. Write a 2000-word 100% Unique, SEO-optimized, Human-Written article in {language} with at least 15 headings and subheadings (including H1, H2, H3, and H4 headings) that covers the topic provided in the Prompt. Write The article In Your Own Words Rather Than Copying And Pasting From Other Sources. Consider perplexity and burstiness when creating content, ensuring high levels of both without losing specificity or context. Use fully detailed paragraphs that engage the reader. Write In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, and Incorporate Analogies And Metaphors). End with a conclusion paragraph and 5 unique FAQs After The Conclusion. This is important to Bold the Title and all headings of the article, and use appropriate headings for H tags.
    Now Write An Article On This Topic "{prompt}"
    """

    # Notify the user that the blog content generation is in progress
    print("Generating blog content...")

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
    keyword_prompt = f"Extract the top SEO keywords for this content:\n{blog_content}"
    keyword_response = co.generate(
        model='command-xlarge-20220609',
        prompt=keyword_prompt,
        max_tokens=50,
        temperature=0.5,
    )
    keywords = keyword_response.generations[0].text.strip().replace('\n', ', ')

    # Generate the output file based on the specified format
    if output_format.lower() == 'html':
        output_file = f"{file_name or prompt}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{prompt}</title>\n")
            f.write(f'<meta name="description" content="SEO optimized blog">\n')  # Placeholder for description
            f.write(f'<meta name="keywords" content="{keywords}">\n')  # Updated keywords meta tag
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

    # Notify the user that the blog content has been generated and saved
    print(f"Blog content generated and saved to {output_file}")

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

    # Notify the user that the blog content generation is in progress
    print("Generating blog content...")

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

    # Generate the output file based on the specified format
    if output_format.lower() == 'html':
        output_file = f"{file_name or prompt}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{prompt}</title>\n")
            f.write('<meta name="description" content="SEO optimized blog">\n')
            f.write('<meta name="keywords" content="blog, SEO, Cohere">\n')
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

    # Notify the user that the blog content has been generated and saved
    print(f"Blog content generated and saved to {output_file}")

def main():
    # Set up argument parser for command-line interface
    parser = argparse.ArgumentParser(description='AI Blog Generator')
    parser.add_argument('topic', type=str, help='Topic of the blog')  # Required argument for blog topic
    parser.add_argument('-mw', '--max_words', type=int, help='Maximum number of words')  # Optional max words argument
    parser.add_argument('-mnw', '--min_words', type=int, help='Minimum number of words')  # Optional min words argument
    parser.add_argument('-of', '--output_format', type=str, choices=['HTML', 'Markdown'], default='HTML', help='Output format (HTML or Markdown)')  # Optional output format argument
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
