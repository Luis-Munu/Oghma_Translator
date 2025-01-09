from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List
from pydantic import field_validator, Field, validator
import json
from dotenv import load_dotenv

load_dotenv()

supported_languages = ['es', 'fr', 'de', 'pt']

class Config(BaseSettings):
    MODEL_API_KEY: str
    base_url: str = Field("https://api.deepseek.com", env="MODEL_URL")
    prompts_path: Path = Path("prompts.json")
    blocked_columns: List[str] = ["author"]
    progress_file: Path = Path("progress.json")
    output_file: Path = Path("Project Oghma Translated.xlsx")
    input_file: Path = Path("Project Oghma.xlsx")
    model: str = Field("deepseek-chat", env="MODEL_NAME")
    temperature: float = 0.3
    save_interval: int = 15000
    max_concurrent_requests: int = 20
    max_retries: int = 5
    retry_delay: float = 1.0
    timeout: float = 30.0
    language: str = 'es'  # Default language

    @field_validator('language')
    def validate_language(cls, v):
        if v not in supported_languages:
            raise ValueError(f'Language must be one of {supported_languages}')
        return v

    @property
    def user_prompt(self) -> str:
        return self._load_prompt('user_prompt')

    @property
    def system_prompt(self) -> str:
        return self._load_prompt('system_prompt')
    
    @property
    def keyword_prompt(self) -> str:
        return self._load_prompt('keyword')

    def _load_prompt(self, prompt_key: str) -> str:
        try:
            with self.prompts_path.open('r', encoding='utf-8') as f:
                prompts = json.load(f)
                language_prompts = prompts.get(self.language, {})
                return language_prompts.get(prompt_key, f"Missing {prompt_key} in prompts.json for language {self.language}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in prompts.json")
        except FileNotFoundError:
            raise FileNotFoundError("prompts.json not found")
        except IOError:
            raise IOError("Failed to read prompts.json")

    @field_validator('temperature')
    def validate_temperature(cls, v):
        if not 0 <= v <= 2:
            raise ValueError('Temperature must be between 0 and 2')
        return v

    @field_validator('save_interval', 'max_concurrent_requests', 'max_retries')
    def validate_positive(cls, v, field):
        if v <= 0:
            raise ValueError(f'{field.name} must be positive')
        return v

    @field_validator('input_file')
    def validate_input_file(cls, v):
        if not v.exists():
            raise FileNotFoundError(f'Input file {v} not found')
        return v