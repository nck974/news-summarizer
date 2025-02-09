from pydantic import BaseModel, ConfigDict


class BaseModelWithConfig(BaseModel):
    """Base model with common configuration"""

    model_config = ConfigDict(from_attributes=True)
