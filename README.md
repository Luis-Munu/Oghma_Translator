# Oghma Translation Assistant
## Overview

The Oghma Translation Assistant is a tool created to facilitate translating the comprehensive "Oghma" document into multiple languages. It leverages AI models—defaulting to DeepSeek but compatible with any OpenAI-compatible API—to handle the translation of all sheets and cells within the document. By using asynchronous calls, it speeds up processing, although translating the entire document still takes a few minutes. The resulting translations are raw and may need additional refinement, particularly for handling issues like names, flags, or class-related terminology.

### Key Features

    Multi-Language Support: Currently supporting spanish, french, portuguese and german but it's easy to add a new language.

    Cost-Effective: Translating the entire Oghma document with DeepSeek v3 costs less than 50 cents.

    Easy to customize: You can easily change the prompts, ignore columns or adapt the logic easily.

    Fully Translated Spanish Version: A fully translated Spanish version of Oghma is available in the output folder.

    Can be stopped during execution: It will continue translating the document where it stopped.

## Getting Started
### Prerequisites

    Python 3.10 or higher

    DeepSeek API key (or other OpenAI compatible API)

### Installation

    Clone the Repository

    git clone https://github.com/Luis-Munu/Oghma_Translator

    Install Dependencies

    pip install -r requirements.txt

    Set Up Environment Variables

    Edit the .env file in the root directory and add your DeepSeek API key, you can change the model here too:

    MODEL_API_KEY=your_deepseek_api_key


### Usage

    Run the Translation Script

    python src/main.py

    Specify Language (Optional)

    By default, the translation is set to French (fr). To translate into another supported language (e.g., Spanish), modify the language parameter in src/config.py:

    language: str = 'es'  # For Spanish

    File Paths

    Ensure that the file paths in src/config.py are correctly set, especially if you're using Windows. The paths are currently in Windows format.

## Configuration
### Configuration File

The src/config.py file contains all the settings for the translation process, including API keys, file paths, and model parameters. You can customize these settings to suit your needs.

    API Key: Set your DeepSeek API key in the .env file.

    Input and Output Files: Modify the input_file and output_file paths to point to your Oghma Excel files.

    Language Support: The supported languages are listed in supported_languages. Feel free to add more languages as long as the encoding supports them.

    Selected language: You can change the language you want to translate Oghma to here.

### Prompts and System Messages

The prompts and system messages used in the translation process are stored in data/prompts.json. You can customize these prompts to improve the quality of the translations.

## Notes
    Contribution: As by the license, you can do whatever you want with the project, feel free to dm me in discord if you got suggestion