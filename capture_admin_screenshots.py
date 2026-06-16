from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineschool.settings')
os.chdir(r"c:\Users\exorc\Downloads\Django Application Development with SQL and Databases")
django.setup()

from courses.models import Course, Lesson, Question, Choice, Submission, SubmissionChoice
from django.contrib.auth import get_user_model

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")

# Create driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Task 3: Capture admin site screenshot
    print("Opening admin site...")
    driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
    
    # Login
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    
    username_input.send_keys("admin")
    password_input.send_keys("admin123")
    
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(2)
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
    )
    
    # Take screenshot
    driver.save_screenshot("03-admin-site.png")
    print("Saved: 03-admin-site.png")
    
    # Task 7: Capture exam result - need to create test data first
    # First, let's check if we have lessons and questions
    User = get_user_model()
    user = User.objects.filter(username="admin").first()
    
    if user:
        # Get or create a lesson with questions
        lesson = Lesson.objects.first()
        if lesson and lesson.questions.exists():
            # Create a submission
            submission = Submission.objects.create(
                user=user,
                lesson=lesson,
                score=7,
                total_points=10
            )
            
            # Add some choices
            choices = Choice.objects.filter(question__lesson=lesson)[:5]
            for choice in choices:
                SubmissionChoice.objects.create(submission=submission, choice=choice)
            
            # Go to exam result page
            driver.get(f"http://127.0.0.1:8000/course/{lesson.course.id}/submission/{submission.id}/result/")
            time.sleep(2)
            driver.save_screenshot("07-final.png")
            print("Saved: 07-final.png")
        else:
            print("No lessons with questions found. Creating test data...")
            # Create test course and lesson
            course = Course.objects.create(
                title="Test Course",
                description="Test Description"
            )
            lesson = Lesson.objects.create(
                course=course,
                title="Test Lesson",
                content="Test Content"
            )
            # Create question
            question = Question.objects.create(
                lesson=lesson,
                question_text="What is Django?",
                points=1
            )
            Choice.objects.create(question=question, choice_text="A framework", is_correct=True)
            Choice.objects.create(question=question, choice_text="A language", is_correct=False)
            
            # Create submission
            submission = Submission.objects.create(
                user=user,
                lesson=lesson,
                score=1,
                total_points=1
            )
            SubmissionChoice.objects.create(
                submission=submission,
                choice=Choice.objects.filter(is_correct=True).first()
            )
            
            driver.get(f"http://127.0.0.1:8000/course/{course.id}/submission/{submission.id}/result/")
            time.sleep(2)
            driver.save_screenshot("07-final.png")
            print("Saved: 07-final.png")

    
    print("Done!")
    
finally:
    driver.quit()
