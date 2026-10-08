import os
import time
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError


load_dotenv()


class LLMService(ABC):
    """
    Base interface for any LLM provider.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class GeminiService(LLMService):
    """
    Gemini implementation of the LLM service.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite",
        )

    def generate(
        self,
        prompt: str,
        max_retries: int = 3,
    ) -> str:

        for attempt in range(max_retries):

            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                if not response.text:
                    raise ValueError(
                        "LLM returned an empty response."
                    )

                return response.text

            except ServerError as exc:

                if attempt == max_retries - 1:
                    raise RuntimeError(
                        "Gemini is temporarily unavailable "
                        "after multiple attempts."
                    ) from exc

                wait_seconds = 2 ** attempt

                print(
                    f"Gemini unavailable. "
                    f"Retrying in {wait_seconds} seconds..."
                )

                time.sleep(wait_seconds)

        raise RuntimeError(
            "Unable to generate LLM response."
        )