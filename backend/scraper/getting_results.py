import requests

BASE_URL = "https://erp.cmr.edu.in"
RESULT_URL_TEMPLATE = f"{BASE_URL}/getStudentSideResultForCMR.json?examScheduleId={{}}&examSemesterId={{}}&universitySyllabusId={{}}"

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
    
if __name__ == "__main__":
    fetch_results()