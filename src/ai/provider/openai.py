"""
Module to use the api of OpenAI
"""

from typing import Any, Iterable, Optional

from loguru import logger
from openai import OpenAI

from src.ai.provider.base import AIModelProtocol, ModelResponse


class OpenAIModel(AIModelProtocol):
    """
    Implementation to use openAI
    """

    used_tokens: int

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
    ):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.used_tokens = 0

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Any = None,
    ) -> ModelResponse:
        """
        Send the provided prompt and return the response
        """
        messages: Iterable = [{"role": "user", "content": prompt}]

        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})

        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=response_format,
        )

        if response.usage is not None:
            logger.debug(
                f"AI prompt took a total of {response.usage.total_tokens} tokens."
            )
            logger.debug(f"Usage: {response.usage.model_dump_json(indent=4)}")
            self.used_tokens += response.usage.total_tokens

        return ModelResponse(
            content=response.choices[0].message.content,
            raw_response=response,
            metadata={
                "model": self.model,
                "finish_reason": response.choices[0].finish_reason,
                "usage": response.usage.model_dump() if response.usage else None,
            },
        )
