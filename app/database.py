
import os
from functools import lru_cache

from sqlalchemy import create_engine, text


@lru_cache
def get_engine():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    return create_engine(
        database_url,
        pool_pre_ping=True
    )


def check_database() -> bool:
    with get_engine().connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar_one() == 1
