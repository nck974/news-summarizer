from typing import List, Optional

from ..database import Database
from ..model.newspaper import Newspaper
from .base_repository import BaseRepository


class NewspaperRepository(BaseRepository[Newspaper]):
    def __init__(self, database: Database):
        self.database = database

    def create(self, newspaper: Newspaper) -> Newspaper:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO newspaper (name, url) VALUES (?, ?)",
                (newspaper.name, newspaper.url),
            )
            conn.commit()
            return Newspaper(
                id=cursor.lastrowid, name=newspaper.name, url=newspaper.url
            )

    def get(self, id: int) -> Optional[Newspaper]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, url FROM newspaper WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return Newspaper.model_validate(dict(row))
            return None

    def get_by_name(self, name: str) -> Optional[Newspaper]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, url FROM newspaper WHERE name = ?", (name,)
            )
            row = cursor.fetchone()
            if row:
                return Newspaper.model_validate(dict(row))
            return None

    def get_all(self) -> List[Newspaper]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, url FROM newspaper")
            return [Newspaper.model_validate(dict(row)) for row in cursor.fetchall()]

    def update(self, newspaper: Newspaper) -> Newspaper:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE newspaper SET name = ?, url = ? WHERE id = ?",
                (newspaper.name, newspaper.url, newspaper.id),
            )
            conn.commit()
            return newspaper

    def delete(self, id: int) -> bool:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM newspaper WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0
