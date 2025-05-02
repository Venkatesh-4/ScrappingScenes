import psycopg2
from backend.database.db_config import DB_CONFIG
import logging

def get_db_connection():
    """Establishes and returns a PostgreSQL database connection."""
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except psycopg2.Error as e:
        logging.error(f"Database connection failed: {e}")
        raise

if __name__ == "__main__":
    get_db_connection()