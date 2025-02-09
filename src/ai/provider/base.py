"""
Interface to define how the ai model shall be implemented
"""

from typing import Protocol, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ModelResponse:
    content: Any
    raw_response: Any
    metadata: Optional[Dict[str, Any]] = None


class AIModelProtocol(Protocol):
    used_tokens: int

    def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> ModelResponse: ...
