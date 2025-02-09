from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """
    Base class to extend any repository
    """

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
