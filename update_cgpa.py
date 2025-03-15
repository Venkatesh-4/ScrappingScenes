def calculate_and_update_cgpa(register_no, cursor):
    cursor.execute("""
        WITH SuccessfulSemesters AS (
            SELECT DISTINCT semester_no
            FROM semesters
            WHERE register_no = %s AND result_status = 'Successful'
        ),
        AllSemesters AS (
            SELECT DISTINCT semester_no
            FROM semesters
            WHERE register_no = %s
        ),
        ComputedCGPA AS (
            SELECT CASE
                WHEN (SELECT COUNT(*) FROM AllSemesters) = (SELECT COUNT(*) FROM SuccessfulSemesters)
                THEN (SELECT SUM(sgpa * earned_credits) / SUM(earned_credits)
                      FROM semesters
                      WHERE register_no = %s AND result_status = 'Successful')
                ELSE NULL
            END AS CGPA
        )
        UPDATE students
        SET cgpa = (SELECT CGPA FROM ComputedCGPA)
        WHERE register_no = %s;
    """, (register_no, register_no, register_no, register_no))

# Runs only when the script is run directly and not when it is imported
if __name__ == "__main__":
    calculate_and_update_cgpa()
