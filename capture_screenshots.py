import mss
import os

# Change to project directory
os.chdir(r"c:\Users\exorc\Downloads\Django Application Development with SQL and Databases")

# Capture full screen
with mss.mss() as sct:
    # Task 3: Admin site screenshot
    sct.shot(output="03-admin-site.png")
    print("Saved: 03-admin-site.png")
    
    # For Task 7, we would need browser window - skip for now
    # Will create placeholder
    print("Task 3 screenshot captured. For Task 7, you'll need to capture the exam result manually.")
