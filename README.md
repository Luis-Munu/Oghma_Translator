# Oghma Translation Assistant
## Overview

The Oghma Translation Assistant is a tool created to facilitate translating the comprehensive "Oghma" document into multiple languages. It leverages AI models—defaulting to DeepSeek but compatible with any OpenAI-compatible API—to handle the translation of all sheets and cells within the document. By using asynchronous calls, it speeds up processing, although translating the entire document still takes a few minutes. The resulting translations are raw and may need additional refinement, particularly for handling issues like names, flags, or class-related terminology.

### Key Features

    Multi-Language Support: Currently supporting 10 languages, adding a new one is as easy as translating the base prompt.

    Cost-Effective: Translating the entire Oghma document with DeepSeek v3 costs less than 50 cents and takes roughly 30 minutes.

    Easy to customize: You can easily change the prompts, add new logic or adapt the parsing easily.

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

Edit the .env file in the root directory and add your DeepSeek API key, you can change the model here too:

    MODEL_API_KEY=your_deepseek_api_key


### Usage

Run the Translation Script

    python src/main.py

Specify Language (Optional)

By default, the translation is set to Spanish (es) and rotates through all the supported languages. To translate into another supported language, modify the language parameter when creating the Config class in src/main.py or simply remove languages from the src/config.py file.

#### File Paths

    Ensure that the file paths in src/config.py are correctly set, especially if you're using Windows. The paths are currently in Windows format.

## Configuration
### Configuration Files

    The src/config.py file contains most of the settings for the translation process, including supported languages, file paths and model parameters. You can customize these settings to suit your needs.

    Set your model API key, url and name in the .env file.

    The JSON files in the data folder contain information related to prompts, direct translation to commonly used terms in Skyrim and parsing information.

## Notes
    Contribution: As by the license, you can do whatever you want with the project, feel free to dm me in discord if you got a suggestion.
