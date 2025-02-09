import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Generator


class Database:
    """
    Object to manage the database: This should be instantiated only once.
    """

    def __init__(self, db_path: str = "news.db"):

        self.db_path = Path(db_path)
        self._create_tables()

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _create_tables(self) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS newspaper (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    url TEXT NOT NULL
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    newspaper_id INTEGER NOT NULL,
                    article TEXT NOT NULL,
                    description TEXT,
                    translation TEXT,
                    category_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (newspaper_id) REFERENCES newspaper (id),
                    FOREIGN KEY (category_id) REFERENCES category (id)
                )
            """
            )

            conn.commit()
