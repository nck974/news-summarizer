from loguru import logger

from src.db.model.newspaper import Newspaper as NewspaperEntity
from src.model.newspaper import Newspaper
from src.db.database import Database
from src.db.repository.newspaper_repository import NewspaperRepository


class NewspaperService:

    newspaper_repository: NewspaperRepository

    def __init__(self, db: Database):
        self.db = db
        self.newspaper_repository = NewspaperRepository(db)

    def save_newspaper(self, newspaper: Newspaper) -> int:
        logger.debug(f"Saving newspaper '{newspaper.name}' in the database...")
        newspaper_entity = self.newspaper_repository.get_by_name(newspaper.name)
        if newspaper_entity is None:
            newspaper_entity = self.newspaper_repository.create(
                NewspaperEntity(name=newspaper.name, url=newspaper.url)
            )

        if newspaper_entity.id is None:
            raise RuntimeError("The newspaper could not be saved")

        return newspaper_entity.id
