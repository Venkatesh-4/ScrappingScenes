import asyncpg
async def get_db_connection():
    return await asyncpg.connect(
        database="cmr_student_database",  # Change "dbname" to "database"
        user="postgres",
        password="venkatesh",
        host="localhost",
        port="5432" 
    )

if __name__ == "__main__":
    get_db_connection()