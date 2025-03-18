import psycopg2
from backend.database.database_config import DB_CONFIG

def get_db_connection():
    """Establishes and returns a PostgreSQL database connection."""
    return psycopg2.connect(**DB_CONFIG)

if __name__ == "__main__":
    get_db_connection()