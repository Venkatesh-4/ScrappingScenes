from backend.lib.utils import clean_value

def insert_semester(student, exam, cursor):
    """Efficiently inserts or updates multiple semester records in the database."""
    query = """
        INSERT INTO semesters (exam_schedule_timetable_id, semester_no, register_no, passing_year, passing_month, sgpa, 
                               total_credits, earned_credits, obtained_marks, out_of_marks, 
                               result_status, block_status, block_reason, ordinance)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (exam_schedule_timetable_id, semester_no, register_no) DO NOTHING;
    """
    values = (clean_value(exam["examScheduleTimetableId"]), clean_value(exam["semesterId"]), clean_value(student["seatNo"]), clean_value(student["passingYear"]), clean_value(student["passingMonth"]), clean_value(student["sgpa"]), 
              clean_value(student["sgpaCreditPointTotal"]), clean_value(student["sgpaEarnedPointsTotal"]), clean_value(student["sgpaObtainedMarks"]), clean_value(student["outOff"]), clean_value(student["resultStatus"]), 
              clean_value(student["resultBlockStatus"]), clean_value(student["resultBlockReason"]), clean_value(student["ordinance"]))
    cursor.execute(query, values) 

    if __name__ == "__main__":
        insert_semester()