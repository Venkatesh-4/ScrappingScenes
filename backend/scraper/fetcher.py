from backend.database.update_cgpa import calculate_and_update_cgpa
from backend.scraper.getting_cookies import login_and_get_cookies
from backend.scraper.getting_exam_schedule import fetch_exam_schedules
from backend.scraper.getting_results import fetch_results
from backend.database.db_connection import get_db_connection
from backend.lib.utils import clean_value
from backend.database.insert_student import insert_student
from backend.database.insert_semester import insert_semester
from backend.database.insert_subject import insert_subject

def main(username: str, password: str):
    print("\n🚀 Starting Script...")
    cookies = login_and_get_cookies(username, password)

    print("\n📊 Retrieving exam schedules...")
    exam_schedules = fetch_exam_schedules(cookies)

    for exam in exam_schedules:
        print(f"\n{'='*50}")
        print(f"📚 Semester: {exam['semesterName']} | Exam: {exam['ExamName']}")
        print(f"📅 Result Declaration Date [YYYY/MM/DD]: {exam['resultDeclarationDate']}")
        print(f"{'='*50}")

        results = fetch_results(cookies, exam['examScheduleId'], exam['semesterId'], exam['universitySyllabusId'])

        if results:
            with get_db_connection() as conn:
                try:
                    with conn.cursor() as cursor:
                        student = results[0]
                        
                        # Extract values once
                        seat_no = clean_value(student.get('seatNo'))
                        semester_no = clean_value(exam.get('semesterId'), int)
                        examScheduleTimetableId = clean_value(exam.get('examScheduleTimetableId', int))

                        # Insert student record first
                        insert_student(student, cursor)

                        # Insert Semesters Data
                        insert_semester(student, exam, cursor)

                        # Batch Insert for Subjects
                        subject_data = [
                            (
                                examScheduleTimetableId,
                                clean_value(sub.get('subjectCode')),
                                semester_no,
                                seat_no,
                                clean_value(sub.get('subjectName')),
                                clean_value(sub.get('InternalMarks'), float),
                                clean_value(sub.get('intPassing'), float),
                                clean_value(sub.get('int'), float),
                                clean_value(sub.get('ExternalMarks'), float),
                                clean_value(sub.get('extPassing'), float),
                                clean_value(sub.get('ext'), float),
                                clean_value(sub.get('Grade')),
                                clean_value(sub.get('Pointer'), float),
                                clean_value(sub.get('earnedCredit'), float),
                                clean_value(sub.get('creditPoint'), float)
                            ) for sub in results
                        ]
                        insert_subject(subject_data, cursor)

                        # Ensure CGPA calculation is part of the same transaction
                        calculate_and_update_cgpa(seat_no, cursor)

                        # Commit only once after all operations succeed
                        conn.commit()
                        print(f"✅ Successfully inserted data for Semester {semester_no}")

                except Exception as e:
                    conn.rollback()  # Rollback if anything fails
                    print(f"❌ Error inserting data: {e}")
                    print("🚨 Transaction rolled back. No changes committed.")


# Runs only when the script is run directly and not when it is imported
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    main(os.getenv('CMR_USERNAME'), os.getenv('CMR_PASSWORD'))
