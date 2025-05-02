from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def setup_driver():
    # Using service since selenium only understands chrome through it
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def login(driver, wait, username, password):
    driver.get("https://saucedemo.com")
    user_name_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    user_name_field.send_keys(username)
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(password)
    # Click login button
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_button.click()

def positive_test():
    print("Results for positive test")
    driver, wait = setup_driver()
    login(driver, wait, "standard_user", "secret_sauce")
    try:
        # Wait for url change
        wait.until(EC.url_contains("inventory.html"))
        cart_element = wait.until(EC.visibility_of_element_located((By.ID, "shopping_cart_container")))
        # Checking if this is inventory page
        current_url = driver.current_url
        assert "inventory.html" in current_url, "Login failed: not on inventory page"
        # Check if shopping cart is displayed
        assert cart_element.is_displayed(), "Login failed: shopping cart not displayed"
        print("Test passed: login successful!")
    except AssertionError as e:
        print(f"Test failed: {str(e)}")
    finally:
        driver.quit()

# Run the test
positive_test()