# AI Blog Article Generator

<p align="center">
    <img src="image/banner.png" alt="Logo" width="90%">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/license-GNU%20GPLv3.0-blue" alt="GitHub license">
   <img src="https://img.shields.io/badge/version-2.0-orange" alt="Version">
    <img src="https://img.shields.io/github/issues/OCEANOFANYTHINGOFFICIAL/AI-Blog-Article-Generator" alt="GitHub issues">
    <img src="https://img.shields.io/github/stars/OCEANOFANYTHINGOFFICIAL/AI-Blog-Article-Generator" alt="GitHub stars">
    <img src="https://img.shields.io/github/forks/OCEANOFANYTHINGOFFICIAL/AI-Blog-Article-Generator" alt="GitHub forks">
    <img src="https://img.shields.io/github/last-commit/OCEANOFANYTHINGOFFICIAL/AI-Blog-Article-Generator" alt="GitHub last commit">
</p>

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Features](#features)
4. [Development](#development)
5. [Usage](#usage)
   - [Command-Line Options](#command-line-options)
6. [Contributing](#contributing)
7. [Code of Conduct](#code-of-conduct)
8. [License](#license)
9. [Why Cohere Instead of OpenAI](#why-cohere-instead-of-openai)

## Introduction

The **AI Blog Article Generator** is a Python-based tool that utilizes the Cohere API to generate high-quality, SEO-optimized blog articles. This tool helps you create engaging, unique, and human-written content based on the specified topic. It can output the content in both HTML and Markdown formats.

## Project Structure

The project is organized as follows:

```plaintext
AI-Blog-Article-Generator/
├── config.py                # Configuration file for API keys
├── aibag.py                 # Main script to generate blog content
├── README.md                # This file
├── contributing.md          # Guidelines for contributing
├── code_of_conduct.md       # Code of Conduct for contributors
└── LICENSE.md               # License information
```

## Features

- **Content Generation:** Create high-quality blog articles with specified topics.
- **SEO Optimization:** Articles are optimized for search engines.
- **Language Support:** Generate content in different languages.
- **Format Options:** Output in HTML, Markdown, and GitHub README formats.
- **Customizable Settings:** Specify maximum and minimum word counts, output format, file name, and language.
- **Enhanced Error Handling:** Advanced functions like timeout and retry for improved reliability.
- **Dynamic Image Integration:** Automatically fetch relevant images from Unsplash based on the topic.

## Development

To develop or contribute to this project, you need Python installed along with the required packages. The primary script (`aibag.py`) uses the `cohere`, `colorama`, `retrying` and `argparse` libraries to interact with the Cohere API and handle command-line arguments.

### Setting Up

1. **Clone the Repository**

   ```bash
   git clone https://github.com/OCEANOFANYTHINGOFFICIAL/AI-Blog-Article-Generator.git
   cd AI-Blog-Article-Generator
   ```

2. **Install Dependencies**

   Make sure to install the necessary Python packages:

   ```bash
   pip install cohere colorama retrying
   ```

   or

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**

   Go to `config.py` file and replace your Cohere API key with the placeholder:

   ```python
   COHERE_API_KEY = 'replace-with-your-cohere-api-key'
   ```

## Usage

The tool is designed to be run from the command line. Here's a detailed explanation of how to use it:

### Command-Line Options

```bash
python aibag.py [topic] [OPTIONS]
```

- **`topic`**: (Required) The main topic of the blog article.

#### Options

- **`-mw` or `--max_words`**: Maximum number of words in the generated article.
  - **Type**: `int`
  - **Example**: `-mw 1500`

- **`-mnw` or `--min_words`**: Minimum number of words in the generated article.
  - **Type**: `int`
  - **Example**: `-mnw 1000`

- **`-of` or `--output_format`**: Format of the output file. Choices are `HTML`, `Markdown`, or `GitHub README`.
  - **Type**: `str`
  - **Default**: `HTML`
  - **Example**: `-of Markdown`

- **`-fn` or `--file_name`**: Name of the output file (without extension).
  - **Type**: `str`
  - **Example**: `-fn my_blog`

- **`-l` or `--language`**: Language of the article. Defaults to `English`.
  - **Type**: `str`
  - **Example**: `-l Spanish`

- **`-gf` or `--github_readme_format`**: Convert content to GitHub README format.
  - **Type**: `flag`
  - **Example**: `-gf`

### Example

Generate a blog article about "The Future of AI" with a maximum length of 1500 words, in HTML format, and name the file `future_of_ai`:

```bash
python aibag.py "The Future of AI" -mw 1500 -of HTML -fn future_of_ai -l English
```

Convert the content to GitHub README format:

```bash
python aibag.py "The Future of AI" -mw 1500 -gf -fn future_of_ai -l English
```

## Contributing

We welcome contributions from the community! If you'd like to contribute to the project, please follow these steps:

1. **Fork the Repository**

2. **Create a Branch**

   ```bash
   git checkout -b feature-branch
   ```

3. **Make Changes**

4. **Commit Your Changes**

   ```bash
   git commit -m "Describe your changes"
   ```

5. **Push to Your Fork**

   ```bash
   git push origin feature-branch
   ```

6. **Create a Pull Request**

For detailed guidelines, refer to the [CONTRIBUTING.md](CONTRIBUTING.md).

## Code of Conduct

We expect everyone to adhere to our Code of Conduct to ensure a welcoming environment. For more details, see the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Why Cohere Instead of OpenAI

We use Cohere for this project because it offers a free tier that meets our needs for generating high-quality content without the cost associated with other APIs, like OpenAI. Cohere's API provides powerful text generation capabilities, making it a suitable choice for creating SEO-optimized articles at no cost.

## Engineered Prompt

The engineered prompt used in the tool is crafted to ensure that the generated content is SEO-optimized, unique, and engaging. It includes:

- **Detailed Instructions**: Specifies the style, format, and structure of the content.
- **SEO Focus**: Ensures that the content is optimized for search engines.
- **Human-Like Writing**: Emphasizes a conversational and engaging tone.

The prompt directs the AI to produce a structured article with headings and subheadings, ensuring comprehensive coverage of the topic.

---

### Summary of Changes

1. **GitHub README Format**: Added support for converting content to GitHub README format using the `-gf` flag.
2. **Enhanced Error Handling**: Included advanced functions like timeout and retry.
3. **Dynamic Image Integration**: Integrated a method to fetch relevant images from Unsplash based on the topic.
4. **Command-Line Updates**: Updated the command-line options to reflect the new features and options.

These updates were necessary to expand the functionality of the tool, improve its robustness, and enhance the user experience.

## Some Notes From The Author

When I build this tool, I had a few key objectives in mind:

1. **Ease of Use**: I wanted to create a tool that was simple to use and required minimal setup.
2. **Quality Content**: I aimed to generate high-quality, SEO-optimized content that could be used for blog articles.
3. **Customization**: I wanted users to have the flexibility to customize the output based on their needs.
4. **Reliability**: I focused on building a tool that was reliable and could handle errors gracefully.
5. **Cost-Effective**: I chose Cohere as the API provider due to its free tier, making it cost-effective for users.
6. **Has The Ability To Generate Content In Different Languages**: I wanted to provide support for generating content in multiple languages.
7. **Dynamic Image Integration**: I integrated image fetching from Unsplash to enhance the visual appeal of the articles.
8. **Community Contribution**: I wanted to create a project that could be contributed to and improved by the community.
9. **SEO Optimization**: I ensured that the content generated was optimized for search engines to improve visibility.
10. **GitHub README Format**: I added support for converting content to GitHub README format for easy integration into repositories.

This tool is indeed designed to be a valuable resource for bloggers, content creators, and developers looking to generate high-quality content quickly and efficiently.

But, This was not easy to build, I had to face many challenges and issues while building this tool. I had to make sure that the content generated was unique, engaging, and human-like. I also had to handle errors, timeouts, and retries to ensure the tool's reliability.

First, I thought of using OpenAI for this project, but due to the cost associated with it, I decided to go with Cohere, which offers a free tier that meets our needs. Cohere's API provides powerful text generation capabilities, making it a suitable choice for creating SEO-optimized articles at no cost.

Then, I had to find an effective way to integrate dynamic images into the articles. I decided to fetch relevant images from Unsplash based on the topic, enhancing the visual appeal of the content. But Unsplah API was not free, so I had to find a way to fetch images.

Eventually, I found an Image API that was free and could be used to fetch images based on the topic. This integration added a new dimension to the tool, making the articles more visually appealing and engaging. The API allowed me to fetch images dynamically and include them in the generated content. Here is the link to the API: [Lorem Flickr](https://loremflickr.com/).

Overall, building this tool was a challenging but rewarding experience.

But Remmember, This tool is not perfect, and there is always room for improvement. I encourage you to contribute to the project, provide feedback, and help make it better. Together, we can create a valuable resource for the community.

I hope you find this tool useful for generating blog articles quickly and efficiently. If you have any feedback, suggestions, or issues, feel free to open an issue or reach out to me directly. I'm always looking to improve the tool and make it more user-friendly.

## Release Notes

This release introduces several significant updates and enhancements to the **AI Blog Article Generator**. These changes include new features, improvements in functionality, and added options to enhance user experience. Below are the detailed updates:

### New Features

#### 1. **GitHub README Format Support**

   - Added support for generating content in GitHub README format. You can now use the `-gf` or `--github_readme_format` flag to convert your blog content into a format suitable for GitHub README files. This new feature helps in creating documentation-style content directly from the tool.

#### 2. **Dynamic Image Integration**

   - Integrated functionality to fetch relevant images from Unsplash based on the topic. This enhancement automatically generates image URLs and inserts them into the content, improving the visual appeal and engagement of the articles.

#### 3. **Enhanced Error Handling**

   - Implemented advanced error handling mechanisms, including timeout and retry options. These improvements ensure that the tool is more reliable and resilient to network issues and other errors during content generation.

### Improvements

#### 1. **Extended Format Options**

   - Added `GitHub README` as an output format option in addition to `HTML` and `Markdown`. Users can now choose the desired format for their output files to better meet their specific needs.

#### 2. **Command-Line Interface Enhancements**

   - Updated the command-line options to include the new `-gf` flag for GitHub README format. The `-of` flag now supports three formats: HTML, Markdown, and GitHub README.

#### 3. **Updated Project Structure**

   - Refined project structure to include support for dynamic image integration and advanced error handling features. This involves adjustments in the codebase and configuration files to accommodate new functionalities.

### Bug Fixes

- Fixed minor bugs related to file naming and formatting issues.
- Resolved issues with language support for non-English content.
- Improved handling of special characters and symbols in the generated content.
