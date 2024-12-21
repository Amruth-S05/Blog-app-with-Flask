from databases import Database
from sqlalchemy import MetaData, create_engine

# SQLite database URL (can be replaced with Postgres or MySQL URLs)
DATABASE_URL = "sqlite:///./blog.db"

# Initialize Database
database = Database(DATABASE_URL)
metadata = MetaData()

# Dependency for accessing the database
async def get_db():
    if not database.is_connected:
        await database.connect()
    return database
