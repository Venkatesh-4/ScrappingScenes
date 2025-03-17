import requests
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
from database_config import DB_CONFIG
from update_cgpa import calculate_and_update_cgpa

# Load environment variables
load_dotenv()

CMR_USERNAME = os.getenv('CMR_USERNAME')
CMR_PASSWORD = os.getenv('CMR_PASSWORD')

# Base URLs
BASE_URL = "https://erp.cmr.edu.in"
LOGIN_URL = f"{BASE_URL}/login.htm"
SCHEDULE_URL = f"{BASE_URL}/getExamScheduleStudentSide.json"
RESULT_URL_TEMPLATE = f"{BASE_URL}/getStudentSideResultForCMR.json?examScheduleId={{}}&examSemesterId={{}}&universitySyllabusId={{}}"

def main():
    """Main function to fetch and store results dynamically."""
    print("\n🚀 Starting Script...")
    cookies = login_and_get_cookies()

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
                        
                        # ✅ Extract values once
                        seat_no = clean_value(student.get('seatNo'))
                        semester_no = clean_value(exam.get('semesterId'), int)
                        examScheduleTimetableId = clean_value(exam.get('examScheduleTimetableId', int))

                        # ✅ Insert student record first
                        insert_student(student, cursor)

                        # ✅ Insert Semesters Data
                        insert_semester(student, exam, cursor)

                        # ✅ Batch Insert for Subjects
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

                        # ✅ Ensure CGPA calculation is part of the same transaction
                        calculate_and_update_cgpa(seat_no, cursor)

                        # ✅ Commit only once after all operations succeed
                        conn.commit()
                        print(f"✅ Successfully inserted data for Semester {semester_no}")

                except Exception as e:
                    conn.rollback()  # 🚨 Rollback if anything fails
                    print(f"❌ Error inserting data: {e}")
                    print("🚨 Transaction rolled back. No changes committed.")





def login_and_get_cookies():
    """Log in using Playwright and retrieve session cookies."""
    print("🟡 Starting Playwright browser...")  
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)  
        page = browser.new_page()

        print(f"🔄 Navigating to login page: {LOGIN_URL}")
        page.goto(LOGIN_URL)

        # **Locate input fields and fill them**
        page.fill('input[name="j_username"]', CMR_USERNAME)  # Adjust selector as needed
        page.fill('input[name="j_password"]', CMR_PASSWORD)
        print("✅ Username and password entered.")

        # Click login button
        page.click('button[type="submit"]')  # Adjust selector if needed
        print("🔄 Clicking login button...")

        # Wait for page to load completely
        page.wait_for_load_state("networkidle")
        print("✅ Login successful, retrieving session cookies.")

        # Extract session cookies
        cookies = page.context.cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        print(f"🍪 Cookies Retrieved: {list(cookie_dict.keys())}")  # Display only cookie names for security

        browser.close()
        return cookie_dict




def fetch_exam_schedules(cookies):
    """Fetch all exam schedules using session cookies."""
    print("🔄 Fetching exam schedules...")
    session = requests.Session()
    session.cookies.update(cookies)

    response = session.get(SCHEDULE_URL)
    print(f"📡 API Response Status: {response.status_code}")

    if response.status_code == 200:
        schedules = response.json()
        print(f"✅ Exam schedules retrieved! Total Semesters: {len(schedules)}")
        return schedules
    else:
        print("❌ Failed to fetch exam schedules.")
        return []

def fetch_results(cookies, examScheduleId, semesterId, universitySyllabusId):
    """Fetch results dynamically for each exam schedule."""
    result_url = RESULT_URL_TEMPLATE.format(examScheduleId, semesterId, universitySyllabusId)
    print(f"🔄 Fetching results from: {result_url}")

    session = requests.Session()
    session.cookies.update(cookies)

    response = session.get(result_url)
    print(f"📡 API Response Status for Semester {semesterId}: {response.status_code}")

    if response.status_code == 200:
        results = response.json()
        print(f"✅ Results retrieved! Subjects: {len(results)}")
        return results
    else:
        print(f"⚠️ Failed to fetch results for Semester {semesterId}.")
        return []


def get_db_connection():
    """Establishes and returns a PostgreSQL database connection."""
    return psycopg2.connect(**DB_CONFIG)

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
        
def clean_value(value, dtype=str):
    """Convert '-' to None and cast to the specified dtype if possible."""
    if value == "-":
        return None
    try:
        return dtype(value.strip())
    except (ValueError, TypeError):
        return None



# Runs only when the script is run directly and not when it is imported
if __name__ == "__main__":
    main()
