import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_CONFIG = os.environ.get(
        "PG_URI",
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:${DB_PORT}/{DB_NAME}".format(
            DB_USER=os.environ.get("PG_USER", "fastapi"),
            DB_PASSWORD=os.environ.get("PG_PASS", "fastapi-password"),
            DB_HOST=os.environ.get("PG_HOST", "fastapi-postgresql"),
            DB_PORT=os.environ.get("PG_PORT", "5432"),
            DB_NAME=os.environ.get("PG_DB", "fastapi"),
        ),
    )


config = Config
