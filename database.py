from databases import Database

# PostgreSQL connection URL (update with your credentials)
DATABASE_URL = "postgresql+asyncpg://postgres:devansh0904@localhost:5432/banks"

# Initialize database instance
database = Database(DATABASE_URL)