from typing import Callable, Optional

from pydantic import Field, BaseModel


class Newspaper(BaseModel):
    """
    Model to represent the configuration of a single newspaper page
    """

    name: str
    url: str
    access_hook: Optional[Callable] = Field(default=None)
    extract_data_hook: Optional[Callable] = Field(default=None)
