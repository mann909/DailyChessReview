from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
from sendSms import sendSms
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = False

user1=os.getenv('DEMO_USERNAME')
password1=os.getenv('DEMO_PASSWORD')

users = [
    {"username": user1, "password": password1},
]

# Set up Chrome options
if not DEBUG :
    options = Options()
    options.add_argument("--headless")  # Enables headless mode
    options.add_argument("--disable-gpu")  # Optional; needed for some headless configurations
    options.add_argument("--no-sandbox")  # Optional; can help prevent crashes in some environments
    options.add_argument("--disable-dev-shm-usage")  # Optional; helps prevent crashes in low memory environments

def login_and_review(username, password):
    # Set up the WebDriver (e.g., for Chrome)
    # Initialize the driver with options
    if not DEBUG : 
        driver = webdriver.Chrome(options=options)
    else :
        driver = webdriver.Chrome()

    # Open the Chess.com login page
    driver.get("https://www.chess.com/login")

    # Find the login fields and log in
    email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    email_input.send_keys(username)

    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    password_input.send_keys(password)
    
    if DEBUG:
        time.sleep(2)
        button = driver.find_element(By.XPATH, "//button[@aria-label='Toggle password visibility']")
        button.click()
        time.sleep(4)


    password_input.send_keys(Keys.RETURN)
    
    print("Successfully Logged in to ",username,"'s Chess account")

    time.sleep(10)  # Wait for login to complete

    # Navigate to the user's game archive
    driver.get(f"https://www.chess.com/games/archive/{username}")

    time.sleep(10)  # Wait for the page to load
    
    links = driver.find_elements(By.CLASS_NAME, "archive-games-link")
    print("Total Number of non-reviewed games : ",len(links))
        
    #extra
    driver.execute_script("arguments[0].scrollIntoView();", links[0])
    # WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.TAG_NAME, "span")))
    driver.execute_script("arguments[0].click();", links[0])

    time.sleep(15)  # Give some time for review to complete
    
    try:
        driver.find_element(By.CSS_SELECTOR, "h3.modal-upgrade-game-review-limit")
        print(username," has already used their daily free review !!")
        sendSms("DAILY CHESS REVIEW : You have already Used Your daily chess review")
    except :
        sendSms("DAILY CHESS REVIEW : Your daily chess.com review was used")
        print("Reviewed the last game for ",username)

    # Close the browser
    driver.quit()

# Run this process for each user
for user in users:
    login_and_review(user["username"], user["password"])
    

