from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineschool.settings')
os.chdir(r"c:\Users\exorc\Downloads\Django Application Development with SQL and Databases")
django.setup()

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Opening admin site...")
    driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
    
    # Login
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys("admin")
    password_input.send_keys("admin123")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
    )
    
    # Take screenshot
    driver.save_screenshot("03-admin-site.png")
    print("Saved: 03-admin-site.png")
    
finally:
    driver.quit()
