# AI Blog Article Generator

<p align="center">
    <img src="image/banner.png" alt="Logo" width="90%">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/license-GNU%20GPLv3.0-blue" alt="GitHub license">
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

``` plaintext
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
- **Format Options:** Output in HTML or Markdown formats.
- **Customizable Settings:** Specify maximum and minimum word counts, output format, file name, and language.

## Development

To develop or contribute to this project, you need Python installed along with the required packages. The primary script (`aibag.py`) uses the `cohere` and `argparse` libraries to interact with the Cohere API and handle command-line arguments.

### Setting Up

1. **Clone the Repository**

   ```bash
   git clone https://github.com/OCEANOFANYTHINGOFFICIAL/AI-Blog-Article-Generator.git
   cd AI-Blog-Article-Generator
   ```

2. **Install Dependencies**

   Make sure to install the necessary Python packages:

   ```bash
   pip install cohere
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

- **`-of` or `--output_format`**: Format of the output file. Choices are `HTML` or `Markdown`.
  - **Type**: `str`
  - **Default**: `HTML`
  - **Example**: `-of Markdown`

- **`-fn` or `--file_name`**: Name of the output file (without extension).
  - **Type**: `str`
  - **Example**: `-fn my_blog`

- **`-l` or `--language`**: Language of the article. Defaults to `English`.
  - **Type**: `str`
  - **Example**: `-l Spanish`

### Example

Generate a blog article about "The Future of AI" with a maximum length of 1500 words, in HTML format, and name the file `future_of_ai`:

```bash
python aibag.py "The Future of AI" -mw 1500 -of HTML -fn future_of_ai -l English
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
