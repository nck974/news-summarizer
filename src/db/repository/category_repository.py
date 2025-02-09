from typing import List, Optional

from ..database import Database
from ..model.category import Category
from .base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, database: Database):
        self.database = database

    def create(self, category: Category) -> Category:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO category (name) VALUES (?)", (category.name,))
            conn.commit()
            return Category(id=cursor.lastrowid, name=category.name)

    def get(self, id: int) -> Optional[Category]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM category WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return Category.model_validate(dict(row))
            return None

    def get_by_name(self, name: str) -> Optional[Category]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM category WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return Category.model_validate(dict(row))
            return None

    def get_all(self) -> List[Category]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM category")
            return [Category.model_validate(dict(row)) for row in cursor.fetchall()]

    def update(self, category: Category) -> Category:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE category SET name = ? WHERE id = ?",
                (category.name, category.id),
            )
            conn.commit()
            return category

    def delete(self, id: int) -> bool:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM category WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0
