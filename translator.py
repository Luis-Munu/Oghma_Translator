from openai import AsyncOpenAI
from asyncio import Semaphore
from config import Config
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import pandas as pd

config = Config()

class TranslationError(Exception):
    pass

class TranslationClientError(TranslationError):
    pass

class TranslationParserError(TranslationError):
    pass

class Translator:
    def __init__(self, client: AsyncOpenAI, semaphore: Semaphore):
        self.client = client
        self.semaphore = semaphore
        self.system_prompt = config.system_prompt  # Use system prompt from config
        self.keyword_prompt = config.keyword_prompt  # Use keyword prompt from config

    def parse_evaluation_response(self, response_text: str) -> str:
        if self.keyword_prompt in response_text:
            return response_text.split(self.keyword_prompt)[1].strip()

        return response_text.strip()

    @retry(
        stop=stop_after_attempt(config.max_retries),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((TranslationClientError, TranslationParserError))
    )
    async def translate_text(self, text: str, sheet_name: str) -> str:
        if not text or pd.isnull(text):
            return ""

        text = str(text).strip()
        if not text:
            return ""

        async with self.semaphore:
            try:
                completion = await self.client.chat.completions.create(
                    model=config.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": config.user_prompt + text}
                    ],
                    temperature=config.temperature
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
                raise TranslationClientError(f"Translation failed: {str(e)}")