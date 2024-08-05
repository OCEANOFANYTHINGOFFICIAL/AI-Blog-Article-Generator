import cohere
import argparse
from config import COHERE_API_KEY

# Initialize the Cohere API client
co = cohere.Client(api_key=COHERE_API_KEY)

def generate_blog(prompt, max_words=None, min_words=None, output_format='HTML', file_name=None):
    # Construct the engineered prompt
    engineered_prompt = f"""
    I Want You To Act As A Content Writer Very Proficient SEO Writer Writes Fluently [TARGETLANGUAGE]. First Create Two Tables. First Table Should be the Outline of the Article and the Second Should be the Article. Bold the Heading of the Second Table using Markdown language. Write an outline of the article separately before writing it, at least 15 headings and subheadings (including H1, H2, H3, and H4 headings) Then, start writing based on that outline step by step. Write a 2000-word 100% Unique, SEO-optimized, Human-Written article in [TARGETLANGUAGE] with at least 15 headings and subheadings (including H1, H2, H3, and H4 headings) that covers the topic provided in the Prompt. Write The article In Your Own Words Rather Than Copying And Pasting From Other Sources. Consider perplexity and burstiness when creating content, ensuring high levels of both without losing specificity or context. Use fully detailed paragraphs that engage the reader. Write In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, and Incorporate Analogies And Metaphors). End with a conclusion paragraph and 5 unique FAQs After The Conclusion. This is important to Bold the Title and all headings of the article, and use appropriate headings for H tags.
    Now Write An Article On This Topic "{prompt}"
    """

    # Add max_words and min_words to the prompt if specified
    if max_words:
        engineered_prompt += f"\nMaximum Words: {max_words}"
    if min_words:
        engineered_prompt += f"\nMinimum Words: {min_words}"

    # Display processing stage to the user
    print("Generating blog content...")

    # Call the Cohere API
    stream = co.chat_stream(
        model='command-r-plus',
        message=engineered_prompt,
        temperature=0.3,
        chat_history=[],
        prompt_truncation='AUTO',
        connectors=[{"id": "web-search"}]
    )

    blog_content = ""
    for event in stream:
        if event.event_type == "text-generation":
            blog_content += event.text

    # Remove unwanted prefixes and format markdown content
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

    # Generate the output file
    if output_format.lower() == 'html':
        output_file = f"{file_name or prompt}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{prompt}</title>\n")
            f.write('<meta name="description" content="SEO optimized blog">\n')
            f.write('<meta name="keywords" content="blog, SEO, Cohere">\n')
            f.write('<script src="https://cdn.jsdelivr.net/gh/OCEANOFANYTHINGOFFICIAL/mdonhtml.js/scripts/mdonhtml.min.js"></script>\n')
            f.write('</head>\n<body>\n')
            f.write('<markdown>\n')
            f.write(blog_content)
            f.write('\n</markdown>\n')
            f.write('<script>\n')
            f.write('document.addEventListener("DOMContentLoaded", function() { mdonhtml(); });\n')
            f.write('</script>\n')
            f.write('\n</body>\n</html>')
    else:
        output_file = f"{file_name or prompt}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(blog_content)

    print(f"Blog content generated and saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='AI Blog Generator')
    parser.add_argument('topic', type=str, help='Topic of the blog')
    parser.add_argument('--max_words', type=int, help='Maximum number of words')
    parser.add_argument('--min_words', type=int, help='Minimum number of words')
    parser.add_argument('--output_format', type=str, choices=['HTML', 'Markdown'], default='HTML', help='Output format (HTML or Markdown)')
    parser.add_argument('--file_name', type=str, help='Output file name')

    args = parser.parse_args()

    if not args.max_words and not args.min_words:
        parser.error('At least one of --max_words or --min_words is required.')

    generate_blog(args.topic, args.max_words, args.min_words, args.output_format, args.file_name)

if __name__ == '__main__':
    main()
