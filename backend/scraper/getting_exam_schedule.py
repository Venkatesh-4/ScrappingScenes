import requests

BASE_URL = "https://erp.cmr.edu.in"
SCHEDULE_URL = f"{BASE_URL}/getExamScheduleStudentSide.json"

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
    
if __name__ == "__main__":
    fetch_exam_schedules()