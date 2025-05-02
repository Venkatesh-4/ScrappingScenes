import os
from urllib.parse import urlparse

def get_db_config():
    """Get database configuration from environment variables or default to local config."""
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Parse the DATABASE_URL provided by Railway
        result = urlparse(database_url)
        return {
            "dbname": result.path[1:],  # Remove leading slash
            "user": result.username,
            "password": result.password,
            "host": result.hostname,
            "port": result.port or "5432"
        }
    else:
        # Local development configuration
        return {
            "dbname": os.getenv("DB_NAME", "cmr_student_database"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "venkatesh"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432")
        }

# Export the config
DB_CONFIG = get_db_config()
