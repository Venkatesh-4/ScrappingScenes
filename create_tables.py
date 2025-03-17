import psycopg2
from database_config import DB_CONFIG

def create_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    queries = [
        """CREATE TABLE IF NOT EXISTS students (
            register_no VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255),
            cgpa REAL,
            course VARCHAR(255),
            school VARCHAR(255),
            course_duration VARCHAR(50)
        )""",
        
        """CREATE TABLE IF NOT EXISTS semesters (
            exam_schedule_timetable_id INT,
            semester_no INT,
            register_no VARCHAR(50),
            passing_year INT,
            passing_month VARCHAR(20),
            sgpa NUMERIC(4,2),
            total_credits REAL,
            earned_credits REAL,
            obtained_marks REAL,
            out_of_marks REAL,
            result_status VARCHAR(50),
            block_status BOOLEAN,
            block_reason TEXT,
            ordinance TEXT,
            PRIMARY KEY (exam_schedule_timetable_id, semester_no, register_no),
            FOREIGN KEY (register_no) REFERENCES students(register_no) ON DELETE CASCADE
        )""",
        
        """CREATE TABLE IF NOT EXISTS subjects (
            exam_schedule_timetable_id INT,
            subject_code VARCHAR(50),
            semester_no INT,
            register_no VARCHAR(50),
            subject_name VARCHAR(255),
            internal_marks REAL,
            internal_passing_marks REAL,
            max_internal_marks REAL,
            external_marks REAL,
            external_passing_marks REAL,
            max_external_marks REAL,
            grade VARCHAR(10),
            grade_point REAL,
            credits_obtained NUMERIC(3,2),
            max_credits NUMERIC(3,2),
            PRIMARY KEY (subject_code, semester_no, register_no, exam_schedule_timetable_id),
            FOREIGN KEY (semester_no, register_no, exam_schedule_timetable_id) REFERENCES semesters(semester_no, register_no, exam_schedule_timetable_id) ON DELETE CASCADE
        )"""
    ]

    for query in queries:
        cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully.")

# Run the function
create_tables()
