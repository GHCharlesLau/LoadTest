import time
import random
import sys
from locust import HttpUser, task, events, between, constant, run_single_user
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException

import logging

# Will be overwritten by locust
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(processName)s] %(message)s",
    handlers=[
        logging.FileHandler("TestResults/test_LocustSelenium.log", encoding="utf-8"),  # write to file
        logging.StreamHandler(sys.stdout)                  # print to console
    ]
)

# record response time manually
def record_custom_task(name, success=True, response_time=0):
    events.request.fire(
        request_type="CUSTOM",
        name=name,
        response_time=response_time,
        response_length=0,
        exception=None if success else Exception("Failed")
    )

class MyUser(HttpUser):
    wait_time = constant(2)
    host = "https://conversation-experiment.onrender.com/join/pekihija"  # Render server
    # host = "https://letschat-43e737e6bc6c.herokuapp.com/join/mehopegu"  # Heroku server

    def start_driver(self):
        """Launch a new Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        try:
            service = Service(log_path="TestResults/chromedriver.log")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logging.info("✅ New driver started")
        except Exception as e:
            logging.error(f"❌ Failed to start driver: {e}")
            self.driver = None

    def on_start(self):
        self.start_driver()
        logging.info(f"A new participant is joining the study...")

    def send_message(self, n=0, max_msg=10, chat_input=None, name="SendMessage1"):
        if chat_input is None:
            raise ValueError("chat_input must be a Selenium WebElement")
        if n >= max_msg:
            return

        time.sleep(random.randint(3, 5))  # Use this to avoid blocking the loop
        start = time.time()
        success = True
        try:
            chat_input.send_keys(f"This is message {n+1}.")
            chat_input.send_keys(Keys.RETURN)  # send the message
        except Exception as e:
            success = False  # if the server response is too slow, mark it as failed
            print(f"Error occurred at {n+1}th message: {e}. Retrying...")
        finally:
            record_custom_task(name, success, response_time=int((time.time() - start) * 1000))

        self.send_message(n + 1, max_msg, chat_input, name)

    @task
    def run_test(self):
        driver = self.driver
        # driver.implicitly_wait(30)
        wait = WebDriverWait(driver, 30)
        session_link = self.host

        def next_page(page_name="NextPage"):
            start = time.time()
            try:
                next_button = wait.until(
                    EC.element_to_be_clickable((By.TAG_NAME, 'button'))
                )
                next_button.click()
                success = True
            except Exception as e:
                success = False
                logging.exception(f"[{page_name}] Failed to click next page button")  # 打印堆栈更有用
            finally:
                elapsed_ms = int((time.time() - start) * 1000)
                record_custom_task(page_name, success, elapsed_ms)

        # Consent page
        start = time.time()
        try:
            success = True
            driver.get(session_link)
        except Exception as e:
            success = False
        finally:
            record_custom_task("ConsentPage", success, int((time.time() - start) * 1000))
        
        time.sleep(random.randint(5, 10))
        next_page("WelcomePage")

        # Welcome page
        try:
            # prolificID = driver.find_element(By.ID, 'id_prolificID')
            prolificID = wait.until(EC.presence_of_element_located((By.ID, 'id_prolificID')))
            prolificID.send_keys('123456781234567812345678')

            # Avatar
            # avatars = driver.find_elements(By.CLASS_NAME, 'persist')
            avatars = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'persist')))
            avatars[random.randint(0, len(avatars)-1)].click()

            # nickname
            # nickname = driver.find_element(By.ID, 'id_nickname')
            nickname = wait.until(EC.presence_of_element_located((By.ID, 'id_nickname')))
            nickname.send_keys('test_bot')
        except Exception as e:
            logging.error(f"Error occurred: {e}")

        time.sleep(random.randint(5, 10))
        next_page("PrimingPage")

        # Priming page
        try:
            # text_box = driver.find_element(By.ID, "id_primingText")
            text_box = wait.until(EC.presence_of_element_located((By.ID, 'id_primingText')))
            text_box.send_keys("This is a test. " * 10)
        except Exception as e:
            logging.error(f"Error occurred: {e}")

        time.sleep(random.randint(10, 15))
        next_page("InstructionPage1")

        # Instruction page ONE
        time.sleep(random.randint(3, 5))
        next_page("WaitingPage1")

        # Waiting page 1
        try:
            wait = WebDriverWait(driver, 120, poll_frequency=3)
            chat_input = wait.until(EC.presence_of_element_located((By.ID, 'chat_input')))  # Explicitly wait for the element to be present
        except Exception as e:
            logging.error(f"Error occurred: {e}")

        # Chat page 1
        self.send_message(0, 10, chat_input, "SendMessage1")

        # Click next button
        time.sleep(5)
        start = time.time()
        try:
            success = True
            # driver.find_element(By.ID, 'nextButton').click()
            wait.until(EC.element_to_be_clickable((By.ID, 'nextButton'))).click()
        except:
            success = False
        finally:
            record_custom_task("IntructionPage2", success, response_time=int((time.time() - start) * 1000))

        # Instruction page TWO
        time.sleep(random.randint(3, 5))
        next_page("WaitingPage2")

        # Waiting page 2
        try:
            wait = WebDriverWait(driver, 120, poll_frequency=3)
            chat_input = wait.until(EC.presence_of_element_located((By.ID, 'chat_input')))
        except Exception as e:
            logging.error(f"Error occurred: {e}")
        
        # Chat page 2
        self.send_message(0, 10, chat_input, "SendMessage2")

        # Click next button
        time.sleep(5)
        start = time.time()
        try:
            success = True
            # driver.find_element(By.ID, 'nextButton').click()
            wait.until(EC.element_to_be_clickable((By.ID, 'nextButton'))).click()
        except:
            success = False
        finally:
            record_custom_task("SurveyPromptPage", success, response_time=int((time.time() - start) * 1000))

        # Survey prompt page
        time.sleep(3)
        next_page("SurveyPage1")

        # Survey page 1
        try:
            id_list = ["id_senA", "id_feeH", "id_CE"]
            for id in id_list:
                for i in range(4):
                    degree = random.randint(0, 6)
                    id_name = f"{id}_{i+1}-{degree}"
                    # driver.find_element(By.ID, id_name).click()
                    wait.until(EC.element_to_be_clickable((By.ID, id_name))).click()
                    time.sleep(3)
        except Exception as e:
            logging.error(f"Error occurred: {e}")

        next_page("SurveyPage2")

        # Survey page 2
        try:
            id_list = ["id_AIU", "id_AIL", "id_partner_label"]

            for id in id_list:
                if id == "id_AIU":
                    id_name = f"{id}-0"
                    # driver.find_element(By.ID, id_name).click()
                    wait.until(EC.element_to_be_clickable((By.ID, id_name))).click()
                    time.sleep(3)
                elif id == "id_AIL":
                    for i in range(4):
                        degree = random.randint(0, 6)
                        id_name = f"{id}_{i+1}-{degree}"
                        # driver.find_element(By.ID, id_name).click()
                        wait.until(EC.element_to_be_clickable((By.ID, id_name))).click()
                        time.sleep(3)
                else:
                    id_name = f"{id}-2"  # "I don't know"
                    # driver.find_element(By.ID, id_name).click()
                    wait.until(EC.element_to_be_clickable((By.ID, id_name))).click()
                    time.sleep(3)
        except Exception as e:
            logging.error(f"Error occurred: {e}")

        next_page("SurveyPage3/Demographics")

        # Survey page 3: Demographics
        try:
            id_list = ["id_age", "id_gender", "id_education", "id_race", "id_partisanship", "id_rlg"]

            # driver.find_element(By.ID, "id_age").send_keys(random.randint(18, 100))
            wait.until(EC.presence_of_element_located((By.ID, "id_age"))).send_keys(random.randint(18, 100))
            time.sleep(3)

            # driver.find_element(By.ID, f"id_gender-3").click()
            wait.until(EC.element_to_be_clickable((By.ID, f"id_gender-3"))).click()
            time.sleep(3)

            # driver.find_element(By.ID, f"id_education-9").click()
            wait.until(EC.element_to_be_clickable((By.ID, f"id_education-9"))).click()
            time.sleep(3)

            # driver.find_element(By.ID, f"id_race-6").click()
            wait.until(EC.element_to_be_clickable((By.ID, f"id_race-6"))).click()
            time.sleep(3)

            # driver.find_element(By.ID, f"id_partisanship-3").click()
            wait.until(EC.element_to_be_clickable((By.ID, f"id_partisanship-3"))).click()
            time.sleep(3)

            for i in range(4):
                degree = random.randint(0, 6)
                # driver.find_element(By.ID, f"id_rlg_{i+1}-{degree}").click()
                wait.until(EC.element_to_be_clickable((By.ID, f"id_rlg_{i+1}-{degree}"))).click()
                time.sleep(3)
        except Exception as e:
            logging.error(f"Error occurred: {e}")

        next_page("PaymentPage")

        # Payment page
        time.sleep(5)


    def on_stop(self):
        self.driver.quit()
        logging.info(f"The participant has finished the study.")


if __name__ == "__main__":
    run_single_user(MyUser)