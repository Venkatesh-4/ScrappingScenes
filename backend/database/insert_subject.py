from psycopg2.extras import execute_values

def insert_subject(subject_data, cursor):
    """Inserts or updates multiple subject records in the database efficiently."""
    query = """
        INSERT INTO subjects (exam_schedule_timetable_id, subject_code, semester_no, register_no, subject_name, 
                              internal_marks, internal_passing_marks, max_internal_marks, 
                              external_marks, external_passing_marks, max_external_marks, 
                              grade, grade_point, credits_obtained, max_credits)
        VALUES %s
        ON CONFLICT (exam_schedule_timetable_id, subject_code, semester_no, register_no) DO NOTHING;
 
    
    """
    execute_values(cursor, query, subject_data) 

if __name__ == "__main__":
    insert_subject()