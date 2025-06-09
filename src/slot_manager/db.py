import psycopg2
from contextlib import contextmanager
from typing import Iterator
from .config import get_env
from .constants import TIME_WINDOW_MINUTES
import time


class PostgresDB:
    def __init__(self, url_env: str):
        self.url = get_env(url_env, required=True)

    @contextmanager
    def connection(self) -> Iterator[psycopg2.extensions.connection]:
        conn = psycopg2.connect(self.url)
        try:
            yield conn
        finally:
            conn.close()

    def upcoming_interviews(self, region: str) -> int:
        start_now = int(time.time())
        end_time = start_now + TIME_WINDOW_MINUTES * 60
        query = (
            "SELECT COUNT(*) FROM interviews WHERE region_allocated = %s "
            "AND start_time BETWEEN %s AND %s"
        )
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (region, start_now, end_time))
                result = cur.fetchone()
                return result[0] if result else 0
