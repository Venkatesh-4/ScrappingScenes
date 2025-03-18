from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

load_dotenv()

CMR_USERNAME = os.getenv('CMR_USERNAME')
CMR_PASSWORD = os.getenv('CMR_PASSWORD')

BASE_URL = "https://erp.cmr.edu.in"
LOGIN_URL = f"{BASE_URL}/login.htm"

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
    
if __name__ == "__main__":
    login_and_get_cookies()