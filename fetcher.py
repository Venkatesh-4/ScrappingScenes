import requests
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import psycopg2
from database_config import DB_CONFIG

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
    """Main function to fetch and print results dynamically."""
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
                    with conn.cursor() as cursor:  # ✅ Correct way to execute transactions
                        cursor.execute("BEGIN;")  # 🚀 Start Transaction

                    semester_no = clean_value(exam.get('semesterId'), int)
                    examScheduleTimetableId = clean_value(exam.get('examScheduleTimetableId', int))
                    student = results[0]
                    seat_no = clean_value(student.get('seatNo'))

                    insert_student(student)  # ✅ Function manages its own cursor
                    
                    for subject in results:
                        semester_data = {
                            "examScheduleTimetableId": examScheduleTimetableId,
                            "semester_no": semester_no,
                            "seatNo": seat_no,
                            "passingYear": clean_value(subject.get('passingYear'), int),
                            "passingMonth": clean_value(subject.get('passingMonth')),
                            "sgpa": clean_value(subject.get('sgpa'), float),
                            "sgpaCreditPointTotal": clean_value(subject.get('sgpaCreditPointTotal'), float),
                            "sgpaEarnedPointsTotal": clean_value(subject.get('sgpaEarnedPointsTotal'), float),
                            "sgpaObtainedMarks": clean_value(subject.get('sgpaObtainedMarks'), float),
                            "outOff": clean_value(subject.get('outOff')),
                            "resultStatus": clean_value(subject.get('resultStatus')),
                            "resultBlockStatus": clean_value(subject.get('resultBlockStatus')),
                            "resultBlockReason": clean_value(subject.get('resultBlockReason')),
                            "ordinance": clean_value(subject.get('ordinance'))
                        }
                        insert_semester(semester_data)  # ✅ Function manages its own cursor

                        subject_data = {
                            "examScheduleTimetableId": examScheduleTimetableId,
                            "subjectCode": clean_value(subject.get('subjectCode')),
                            "semester_no": semester_no,
                            "seatNo": seat_no,
                            "subjectName": clean_value(subject.get('subjectName')),
                            "InternalMarks": clean_value(subject.get('InternalMarks'), float),
                            "intPassing": clean_value(subject.get('intPassing'), float),
                            "int": clean_value(subject.get('int'), float),
                            "ExternalMarks": clean_value(subject.get('ExternalMarks'), float),
                            "extPassing": clean_value(subject.get('extPassing'), float),
                            "ext": clean_value(subject.get('ext'), float),
                            "Grade": clean_value(subject.get('Grade')),
                            "Pointer": clean_value(subject.get('Pointer'), float),
                            "earnedCredit": clean_value(subject.get('earnedCredit'), float),
                            "creditPoint": clean_value(subject.get('creditPoint'), float)
                        }
                        insert_subject(subject_data)  # ✅ Function manages its own cursor

                        print(f"✅ Data inserted for {clean_value(subject.get('subjectName'), str)}")

                    conn.commit()  # ✅ Commit Transaction
                    print("✅ All data inserted successfully.")

                except Exception as e:
                    conn.rollback()  # 🚨 Rollback if anything fails
                    print(f"❌ Error inserting data: {e}")
                    print("🚨 Transaction rolled back. No changes committed.")

        else:
            print("🚫 No results available.")




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

# Function to connect to the database
import psycopg2
from database_config import DB_CONFIG

def get_db_connection():
    """Establishes and returns a PostgreSQL database connection."""
    return psycopg2.connect(**DB_CONFIG)

def insert_student(student):
    """Inserts or updates student details in the database."""
    query = """
        INSERT INTO students (register_no, name, course, school, course_duration)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (register_no) DO UPDATE 
        SET name = EXCLUDED.name, 
            course = EXCLUDED.course, 
            school = EXCLUDED.school, 
            course_duration = EXCLUDED.course_duration;
    """
    
    values = (student["seatNo"], student["studentName"], student["programName"], 
              student["instituteName"], student["academicyear"])
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values)

def insert_semester(semester):
    """Inserts or updates semester details in the database."""
    query = """
        INSERT INTO semesters (exam_schedule_timetable_id, semester_no, register_no, passing_year, passing_month, sgpa, 
                               total_credits, earned_credits, obtained_marks, out_of_marks, 
                               result_status, block_status, block_reason, ordinance)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (exam_schedule_timetable_id, semester_no, register_no) DO UPDATE 
        SET passing_year = EXCLUDED.passing_year,
            passing_month = EXCLUDED.passing_month,
            sgpa = EXCLUDED.sgpa,
            total_credits = EXCLUDED.total_credits,
            earned_credits = EXCLUDED.earned_credits,
            obtained_marks = EXCLUDED.obtained_marks,
            out_of_marks = EXCLUDED.out_of_marks,
            result_status = EXCLUDED.result_status,
            block_status = EXCLUDED.block_status,
            block_reason = EXCLUDED.block_reason,
            ordinance = EXCLUDED.ordinance;
    """
    
    values = (semester["examScheduleTimetableId"], semester["semester_no"], semester["seatNo"], semester["passingYear"], 
              semester["passingMonth"], semester["sgpa"], semester["sgpaCreditPointTotal"], 
              semester["sgpaEarnedPointsTotal"], semester["sgpaObtainedMarks"], 
              semester["outOff"], semester["resultStatus"], semester["resultBlockStatus"], 
              semester["resultBlockReason"], semester["ordinance"])
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values)

def insert_subject(subject):
    """Inserts or updates subject details in the database."""
    query = """
        INSERT INTO subjects (exam_schedule_timetable_id, subject_code, semester_no, register_no, subject_name, 
                              internal_marks, internal_passing_marks, max_internal_marks, 
                              external_marks, external_passing_marks, max_external_marks, 
                              grade, grade_point, credits_obtained, max_credits)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (exam_schedule_timetable_id, subject_code, semester_no, register_no) DO UPDATE 
        SET subject_name = EXCLUDED.subject_name,
            internal_marks = EXCLUDED.internal_marks,
            internal_passing_marks = EXCLUDED.internal_passing_marks,
            max_internal_marks = EXCLUDED.max_internal_marks,
            external_marks = EXCLUDED.external_marks,
            external_passing_marks = EXCLUDED.external_passing_marks,
            max_external_marks = EXCLUDED.max_external_marks,
            grade = EXCLUDED.grade,
            grade_point = EXCLUDED.grade_point,
            credits_obtained = EXCLUDED.credits_obtained,
            max_credits = EXCLUDED.max_credits;
    """
    
    values = (subject["examScheduleTimetableId"], subject["subjectCode"], subject["semester_no"], subject["seatNo"], subject["subjectName"], 
              subject["InternalMarks"], subject["intPassing"], subject["int"], 
              subject["ExternalMarks"], subject["extPassing"], subject["ext"], 
              subject["Grade"], subject["Pointer"],subject["earnedCredit"], subject["creditPoint"])
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values)
        
def clean_value(value, dtype=str):
    """Convert '-' to None and cast to the specified dtype if possible."""
    if value == "-":
        return None
    try:
        return dtype(value)
    except (ValueError, TypeError):
        return None



# Runs only when the script is run directly and not when it is imported
if __name__ == "__main__":
    main()
