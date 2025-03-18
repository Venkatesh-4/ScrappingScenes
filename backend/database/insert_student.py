from backend.lib.utils import clean_value

def insert_student(student, cursor):
    """Inserts or updates student details in the database."""
    query = """
        INSERT INTO students (register_no, name, course, school, course_duration)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (register_no) DO NOTHING
    """
    
    values = (clean_value(student["seatNo"]), clean_value(student["studentName"]), clean_value(student["programName"]), 
              clean_value(student["instituteName"]), clean_value(student["academicyear"]))
    

    cursor.execute(query, values)

    if __name__ == "__main__":
        insert_student()