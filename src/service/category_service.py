from loguru import logger

from src.db.database import Database
from src.db.model.category import Category
from src.db.repository.category_repository import CategoryRepository


class CategoryService:

    category_repository: CategoryRepository

    def __init__(self, db: Database):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def save_category(self, category_name: str) -> int:
        logger.debug(f"Saving category '{category_name}' in the database...")
        category = self.category_repository.get_by_name(category_name)
        if category is None:
            category = self.category_repository.create(Category(name=category_name))

        if category.id is None:
            raise RuntimeError("The category could not be saved")

        return category.id
