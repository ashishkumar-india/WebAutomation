from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
import traceback
import os


def automate_login(url, username, password):
    """
    Automates login and clicks a specific href link after login.
    """
    driver = None
    try:
        print("Starting Chrome WebDriver...")
        
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 15)

        print(f"Opening {url}...")
        driver.get(url)

        # Wait for and fill username
        print("Waiting for username input...")
        username_field = wait.until(
            EC.presence_of_element_located((By.NAME, "LoginForm[username]"))
        )
        username_field.clear()
        username_field.send_keys(username)

        # Wait for and fill password
        print("Waiting for password input...")
        password_field = wait.until(
            EC.presence_of_element_located((By.NAME, "LoginForm[password]"))
        )
        password_field.clear()
        password_field.send_keys(password)

        # Submit login
        print("Waiting for login button...")
        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        print("Clicking login button...")
        login_button.click()

        # Wait for post-login and click target link
        target_href = "/index.php/vidhyarthi/programme/index?prg_id=66dfabcbab5e1456039f9ee4a0fa65c3d92f11d4647fa15cb630804a821f313e2089"
        print(f"Waiting for link with href '{target_href}'...")
        
        href_selector = f"a[href='{target_href}']"
        href_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, href_selector))
        )

        print("Clicking the target href link...")
        href_link.click()

        # Wait for page to load after click
        print("Waiting for page to load...")
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        print("Automation completed successfully!")
        input("Press Enter to close browser...")  # Keep browser open for inspection

    except TimeoutException as e:
        print(f"Timeout error: Element not found within wait time")
        print(traceback.format_exc())
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        print(traceback.format_exc())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(traceback.format_exc())
    finally:
        if driver:
            print("Closing browser...")
            driver.quit()  # Properly close browser and end session


if __name__ == '__main__':
    WEBSITE_URL = 'https://cusb.samarth.edu.in/index.php/site/login'
    
    # Better: Load from environment variables
    YOUR_USERNAME = os.getenv('CUSB_USERNAME', 'CUSB2402332007')
    YOUR_PASSWORD = os.getenv('CUSB_PASSWORD', 'Shish#878')
    
    automate_login(WEBSITE_URL, YOUR_USERNAME, YOUR_PASSWORD)
