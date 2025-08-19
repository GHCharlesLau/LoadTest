import time
import random
from locust import task, constant, events, run_single_user, HttpUser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class test_user(HttpUser):
    host = "http://localhost:8000/join/giheroba"
    wait_time = constant(1)

    def on_start(self):
        # Optional：Configure headless browsers（Do not display the window）
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')  # 规避某些系统或 Chrome 版本下的 bug
        chrome_options.add_argument('--no-sandbox')  # 对 Linux 容器很有用
        chrome_options.add_argument('--disable-dev-shm-usage')  # 避免内存问题（Docker 中常用）

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(15)

        driver.get(self.host)  # Join the room
        self.driver = driver

    def on_stop(self):
        self.driver.quit()

    @task
    def run_test(self):
        driver = self.driver
        # Add your test code here
        try:
            # Consent page
            def next_page():
                next_button = driver.find_element(By.TAG_NAME, 'button')
                next_button.click()

            time.sleep(random.randint(5, 10))
            next_page()

            # Welcome page
            prolificID = driver.find_element(By.ID, 'id_prolificID')
            prolificID.send_keys('123456781234567812345678')

            # Avatar
            avatars = driver.find_elements(By.CLASS_NAME, 'persist')
            avatars[random.randint(0, len(avatars)-1)].click()

            # nickname
            nickname = driver.find_element(By.ID, 'id_nickname')
            nickname.send_keys('test_bot')

            time.sleep(random.randint(5, 10))
            next_page()

            # Priming page
            text_box = driver.find_element(By.ID, "id_primingText")
            text_box.send_keys("This is a test. " * 10)
            time.sleep(random.randint(10, 15))
            next_page()

            # Instruction page ONE
            time.sleep(random.randint(5, 10))
            next_page()

            # Waiting page
            # driver.implicitly_wait(15)
            wait = WebDriverWait(driver, 15)

            # Chat page 1
            # chat_input = driver.find_element(By.ID, 'chat_input')
            chat_input = wait.until(EC.presence_of_element_located((By.ID, 'chat_input')))  # Explicitly wait for the element to be present

            for i in range(5):
                chat_input.send_keys(f"This is message {i}.")
                chat_input.send_keys(Keys.RETURN)  # send the message
                time.sleep(random.randint(5, 10))

            # Click next button
            for i in range(3):
                try:
                    driver.find_element(By.ID, 'nextButton').click()
                    time.sleep(2)
                except:
                    pass

            # Instruction page TWO
            time.sleep(random.randint(5, 10))
            next_page()

            # Waiting page
            # driver.implicitly_wait(15)
            wait = WebDriverWait(driver, 15)

            # Chat page 2
            chat_input = wait.until(EC.presence_of_element_located((By.ID, 'chat_input')))
            # chat_input = driver.find_element(By.ID, 'chat_input')

            for i in range(5):
                chat_input.send_keys(f"This is message {i}.")
                chat_input.send_keys(Keys.RETURN)  # send the message
                time.sleep(random.randint(5, 10))

            # Click next button
            for i in range(3):
                try:
                    driver.find_element(By.ID, 'nextButton').click()
                    time.sleep(2)
                except:
                    pass

            # Survey prompt page
            time.sleep(3)
            next_page()

            # Survey page 1
            id_list = ["id_senA", "id_feeH", "id_CE"]
            for id in id_list:
                for i in range(4):
                    degree = random.randint(0, 6)
                    id_name = f"{id}_{i+1}-{degree}"
                    driver.find_element(By.ID, id_name).click()
                    time.sleep(3)

            next_page()

            # Survey page 2
            id_list = ["id_AIU", "id_AIL", "id_partner_label"]

            for id in id_list:
                if id == "id_AIU":
                    id_name = f"{id}-0"
                    driver.find_element(By.ID, id_name).click()
                    time.sleep(3)
                elif id == "id_AIL":
                    for i in range(4):
                        degree = random.randint(0, 6)
                        id_name = f"{id}_{i+1}-{degree}"
                        driver.find_element(By.ID, id_name).click()
                        time.sleep(3)
                else:
                    id_name = f"{id}-2"  # "I don't know"
                    driver.find_element(By.ID, id_name).click()
                    time.sleep(3)

            next_page()

            # Survey page 3: Demographics
            id_list = ["id_age", "id_gender", "id_education", "id_race", "id_partisanship", "id_rlg"]

            driver.find_element(By.ID, "id_age").send_keys(random.randint(18, 100))
            time.sleep(3)

            driver.find_element(By.ID, f"id_gender-3").click()
            time.sleep(3)

            driver.find_element(By.ID, f"id_education-9").click()
            time.sleep(3)

            driver.find_element(By.ID, f"id_race-6").click()
            time.sleep(3)

            driver.find_element(By.ID, f"id_partisanship-3").click()
            time.sleep(3)

            for i in range(4):
                degree = random.randint(0, 6)
                driver.find_element(By.ID, f"id_rlg_{i+1}-{degree}").click()
                time.sleep(3)

            next_page()
            # close the browser
            driver.quit()
        except Exception as e:
            logger.error(f"Error initializing Chrome driver: {e}")
            raise
        finally:
            driver.quit()

if __name__ == "__main__":
    run_single_user(test_user)