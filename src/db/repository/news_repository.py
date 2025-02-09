from typing import Optional

from ..database import Database
from ..entity.news import News
from .base_repository import BaseRepository


class NewsRepository(BaseRepository[News]):
    def __init__(self, database: Database):
        self.database = database

    def create(self, news: News) -> News:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO news 
                   (newspaper_id, article, description, translation, category_id)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    news.newspaper_id,
                    news.article,
                    news.description,
                    news.translation,
                    news.category_id,
                ),
            )
            conn.commit()
            created_news = news.model_copy(update={"id": cursor.lastrowid})
            return created_news

    def get(self, id: int) -> Optional[News]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, newspaper_id, article, description, translation,
                          category_id, created_at
                   FROM news WHERE id = ?""",
                (id,),
            )
            row = cursor.fetchone()
            if row:
                return News.model_validate(dict(row))
            return None

    def get_all(self) -> list[News]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, newspaper_id, article, description, translation,
                          category_id, created_at FROM news"""
            )
            return [News.model_validate(dict(row)) for row in cursor.fetchall()]

    def get_by_category(self, category_id: int) -> list[News]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, newspaper_id, article, description, translation,
                          category_id, created_at
                   FROM news WHERE category_id = ?""",
                (category_id,),
            )
            return [News.model_validate(dict(row)) for row in cursor.fetchall()]

    def get_by_name(self, name: str) -> Optional[News]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, newspaper_id, article, description, translation,
                          category_id, created_at
                   FROM news WHERE article = ?""",
                (name,),
            )
            row = cursor.fetchone()
            if row:
                return News.model_validate(dict(row))
            return None

    def update(self, news: News) -> News:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE news 
                   SET newspaper_id = ?, article = ?, 
                       description = ?, category_id = ?, translation = ?
                   WHERE id = ?""",
                (
                    news.newspaper_id,
                    news.article,
                    news.description,
                    news.category_id,
                    news.translation,
                    news.id,
                ),
            )
            conn.commit()
            return news

    def delete(self, id: int) -> bool:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM news WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0
