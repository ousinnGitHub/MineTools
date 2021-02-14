import pause
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
import logging.config


NIKE_JP_HOME_URL = 'https://www.nike.com/jp/login'


def run(driver, username, password):
    driver.maximize_window()
    driver.set_page_load_timeout(300)

    skip_retry_login = True
    try:
        login(driver=driver, username=username, password=password)
    except TimeoutException:
        skip_retry_login = False
        print("Failed to login due to timeout. Retrying...")
    except Exception as e:
        print("Failed to login: " + str(e))
        # driver.close()

    if skip_retry_login is False:
        try:
            retry_login(driver=driver, username=username, password=password)
        except Exception as e:
            print("Failed to retry login: " + str(e))

def login(driver, username, password):
    try:
        print("Requesting page: " + NIKE_JP_HOME_URL)
        driver.get(NIKE_JP_HOME_URL)
    except TimeoutException:
        print("Page load timed out but continuing anyway")

    print("Waiting for login fields to become visible")
    wait_until_visible(driver=driver, xpath="//input[@name='emailAddress']")

    print("Entering username and password")
    email_input = driver.find_element_by_xpath("//input[@name='emailAddress']")
    email_input.clear()
    email_input.send_keys(username)

    time.sleep(1)
    pwd_input = driver.find_element_by_xpath("//input[@name='password']")
    pwd_input.clear()
    pwd_input.send_keys(password)

    time.sleep(1)
    print("Logging in")
    driver.find_element_by_xpath("//input[@value='ログイン']").click()

    wait_until_visible(driver=driver, xpath="//a[@data-path='myAccount:greeting']", duration=5)
    print("Successfully logged in")


def retry_login(driver, username, password):
    num_retries_attempted = 0
    num_retries = 5
    while True:
        try:
            # Xpath to error dialog button
            # / html / body / div[2] / div[3] / div[4] / div / div[2] / input
            xpath = "/html/body/div[2]/div[3]/div[4]/div/div[2]/input"
            wait_until_visible(driver=driver, xpath=xpath, duration=5)
            driver.find_element_by_xpath(xpath).click()

            password_input = driver.find_element_by_xpath("//input[@name='password']")
            password_input.clear()
            password_input.send_keys(password)

            print("Logging in")

            try:
                driver.find_element_by_xpath("//input[@value='ログイン']").click()
            except Exception as e:
                print(str(e))
                if num_retries_attempted < num_retries:
                    num_retries_attempted += 1
                    continue
                else:
                    print("Too many login attempts. Please restart app.")
                    break

            if num_retries_attempted < num_retries:
                num_retries_attempted += 1
                continue
            else:
                print("Too many login attempts. Please restart app.")
                break
        except Exception as e:
            print("Error dialog did not load, proceed. Error: " + str(e))
        break

    wait_until_visible(driver=driver, xpath="//a[@data-path='myAccount:greeting']")
    print("Successfully logged in")


def wait_until_visible(driver, xpath=None, class_name=None, el_id=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(ec.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(ec.visibility_of_element_located((By.CLASS_NAME, class_name)))
    elif el_id:
        WebDriverWait(driver, duration, frequency).until(ec.visibility_of_element_located((By.ID, el_id)))


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    isHeadless = False
    if isHeadless:
        options.add_argument("headless")
    executable_path = "./bin/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=executable_path, options=options)

    username = "sinnoukunn@gmail.com"
    password = "Wangchen0507."

    run(driver=driver, username=username, password=password)
