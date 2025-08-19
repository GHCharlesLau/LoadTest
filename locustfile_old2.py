import time
import random
from locust import task, constant, events, run_single_user, HttpUser
from locust_plugins.users.webdriver import WebdriverUser
from locust_plugins.listeners import RescheduleTaskOnFail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class test_user(WebdriverUser):
    host = "http://localhost:8000/join/giheroba"
    wait_time = constant(1)
    # webdriver client options can be customized by overriding the option_args
    option_args = [
        "--disable-translate",
        "--disable-extensions",
        "--disable-background-networking",
        "--safebrowsing-disable-auto-update",
        "--disable-sync",
        "--metrics-recording-only",
        "--disable-default-apps",
        "--no-first-run",
        "--disable-setuid-sandbox",
        "--hide-scrollbars",
        "--no-sandbox",
        "--no-zygote",
        "--autoplay-policy=no-user-gesture-required",
        "--disable-notifications",
        "--disable-logging",
        "--disable-permissions-api",
        "--ignore-certificate-errors",
    ]

    if __name__ == "__main__":
        # wait a bit at the end to make debugging easier
        wait_time = constant(5)
    else:
        # headless by default if running real locust and not just debugging
        headless = True

    def on_start(self):
        self.client.set_window_size(1400, 1000)
        self.client.implicitly_wait(5)

    def on_stop(self):
        self.client.quit()

    @task
    def lets_chat(self):
        self.clear()
        self.client.start_time = time.monotonic()  # to measure the time from now to first locust_find_element finishes
        scenario_start_time = self.client.start_time  # to measure the time for the whole scenario

        try:
            self.client.get("")

            # Consent page
            def next_page():
                next_button = self.client.find_element(By.TAG_NAME, 'button')
                next_button.click()

            time.sleep(random.randint(5, 10))
            next_page()

            # Welcome page
            prolificID = self.client.find_element(By.ID, 'id_prolificID')
            prolificID.send_keys('123456781234567812345678')

            # Avatar
            avatars = self.client.find_elements(By.CLASS_NAME, 'persist')
            avatars[random.randint(0, len(avatars)-1)].click()

            # nickname
            nickname = self.client.find_element(By.ID, 'id_nickname')
            nickname.send_keys('test_bot')

            time.sleep(random.randint(5, 10))
            next_page()

            # Priming page
            text_box = self.client.find_element(By.ID, "id_primingText")
            text_box.send_keys("This is a test. " * 10)
            time.sleep(random.randint(10, 15))
            next_page()

            # Instruction page ONE
            time.sleep(random.randint(5, 10))
            next_page()

            # Waiting page
            # self.client.implicitly_wait(15)
            wait = WebDriverWait(self.client, 15)

            # Chat page 1
            # chat_input = self.client.find_element(By.ID, 'chat_input')
            chat_input = wait.until(EC.presence_of_element_located((By.ID, 'chat_input')))  # Explicitly wait for the element to be present

            for i in range(5):
                chat_input.send_keys(f"This is message {i}.")
                chat_input.send_keys(Keys.RETURN)  # send the message
                time.sleep(random.randint(5, 10))

            # Click next button
            for i in range(3):
                try:
                    self.client.find_element(By.ID, 'nextButton').click()
                    time.sleep(2)
                except:
                    pass

            # Instruction page TWO
            time.sleep(random.randint(5, 10))
            next_page()

            # Waiting page
            # self.client.implicitly_wait(15)
            wait = WebDriverWait(self.client, 15)

            # Chat page 2
            chat_input = wait.until(EC.presence_of_element_located((By.ID, 'chat_input')))
            # chat_input = self.client.find_element(By.ID, 'chat_input')

            for i in range(5):
                chat_input.send_keys(f"This is message {i}.")
                chat_input.send_keys(Keys.RETURN)  # send the message
                time.sleep(random.randint(5, 10))

            # Click next button
            for i in range(3):
                try:
                    self.client.find_element(By.ID, 'nextButton').click()
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
                    self.client.find_element(By.ID, id_name).click()
                    time.sleep(3)

            next_page()

            # Survey page 2
            id_list = ["id_AIU", "id_AIL", "id_partner_label"]

            for id in id_list:
                if id == "id_AIU":
                    id_name = f"{id}-0"
                    self.client.find_element(By.ID, id_name).click()
                    time.sleep(3)
                elif id == "id_AIL":
                    for i in range(4):
                        degree = random.randint(0, 6)
                        id_name = f"{id}_{i+1}-{degree}"
                        self.client.find_element(By.ID, id_name).click()
                        time.sleep(3)
                else:
                    id_name = f"{id}-2"  # "I don't know"
                    self.client.find_element(By.ID, id_name).click()
                    time.sleep(3)

            next_page()

            # Survey page 3: Demographics
            id_list = ["id_age", "id_gender", "id_education", "id_race", "id_partisanship", "id_rlg"]

            self.client.find_element(By.ID, "id_age").send_keys(random.randint(18, 100))
            time.sleep(3)

            self.client.find_element(By.ID, f"id_gender-3").click()
            time.sleep(3)

            self.client.find_element(By.ID, f"id_education-9").click()
            time.sleep(3)

            self.client.find_element(By.ID, f"id_race-6").click()
            time.sleep(3)

            self.client.find_element(By.ID, f"id_partisanship-3").click()
            time.sleep(3)

            for i in range(4):
                degree = random.randint(0, 6)
                self.client.find_element(By.ID, f"id_rlg_{i+1}-{degree}").click()
                time.sleep(3)

            next_page()

        except Exception as e:
            logger.error(f"An error occurred: {e}")

        finally:
            # close the browser
            self.client.quit()

        self.environment.events.request.fire(
        request_type="flow",
        name="Participate in the experiment",
        response_time=(time.monotonic() - scenario_start_time) * 1000,
        response_length=0,
        exception=None,
        )

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    RescheduleTaskOnFail(environment)


if __name__ == "__main__":
    run_single_user(test_user)

