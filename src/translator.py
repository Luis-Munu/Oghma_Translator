from openai import AsyncOpenAI
from asyncio import Semaphore
from config import Config
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import pandas as pd

class TranslationError(Exception):
    pass

class TranslationClientError(TranslationError):
    pass

class TranslationParserError(TranslationError):
    pass

class Translator:
    def __init__(self, client: AsyncOpenAI, semaphore: Semaphore, config: Config):
        self.client = client
        self.semaphore = semaphore
        self.config = config
        self.system_prompt = config.system_prompt
        self.keyword_start_prompt = config.keyword_start_prompt
        self.keyword_end_prompt = config.keyword_end_prompt

    def parse_evaluation_response(self, response_text: str) -> str:
        if self.keyword_start_prompt in response_text and self.keyword_end_prompt in response_text:
            return response_text.split(self.keyword_start_prompt)[1].strip().split(self.keyword_end_prompt)[0].strip()
        return response_text.strip()

    def _replace_known_terms(self, text: str) -> str:
        """Replace known terms in the text using the knowledge base"""
        if not text:
            return text
            
        # Create case-insensitive mapping of terms to their original case
        term_mapping = {term.lower(): term for term in self.config.knowledge.keys()}
        
        # Split text into words while preserving whitespace and punctuation
        words = text.split()
        for i, word in enumerate(words):
            # Check lowercase version against knowledge base
            lower_word = word.lower()
            if lower_word in term_mapping:
                # Get the original term and its translation
                original_term = term_mapping[lower_word]
                translation = self.config.knowledge[original_term].get(self.config.language, original_term)
                
                # Preserve original capitalization by replacing with same case pattern
                if word.isupper():
                    translation = translation.upper()
                elif word.istitle():
                    translation = translation.title()
                    
                words[i] = word.replace(original_term, translation)
                
        return ' '.join(words)

    async def translate_text(self, text: str, sheet_name: str) -> str:
        @retry(
            stop=stop_after_attempt(self.config.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=10),
            retry=retry_if_exception_type((TranslationClientError, TranslationParserError))
        )
        async def _translate_text_with_retry(text: str) -> str:
            if not text or pd.isnull(text):
                return ""

            text = str(text).strip()
            if not text:
                return ""
                
            # Replace known terms before translation
            text = self._replace_known_terms(text)

            async with self.semaphore:
                try:
                    completion = await self.client.chat.completions.create(
                        model=self.config.model,
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": self.config.user_prompt + text}
                        ],
                        temperature=self.config.temperature
                    )

                    if not completion.choices:
                        raise TranslationClientError("No choices returned from API")

                    response_text = completion.choices[0].message.content
                    if not response_text:
                        raise TranslationClientError("Empty response from API")

                    translation = self.parse_evaluation_response(response_text)
                    if not translation:
                        raise TranslationParserError("Parsed translation is empty")

                    return translation

                except Exception as e:
                    if isinstance(e, TranslationClientError):
                        raise
                    raise TranslationClientError(f"Translation failed: {str(e)}") from e

        return await _translate_text_with_retry(text)
