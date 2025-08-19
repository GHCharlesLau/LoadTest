import time
import random
import re, sys, os
from bs4 import BeautifulSoup
from locust import HttpUser, task, TaskSet, between, constant, run_single_user
import logging

# Will be overwritten by locust (Configure this in locust.conf, or set in headless mode)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(processName)s] %(message)s",
    handlers=[
        logging.FileHandler("TestResults/test_locust_new.log", encoding="utf-8"),  # write to file
        logging.StreamHandler(sys.stdout)                  # print to console
    ]
)

class UserTask(TaskSet):
    def next_page(self, url, data=None, name="NextPage"):
        with self.client.post(url=url, data=data, name=name) as resp: 
            next_url = resp.url
            logging.info(f"Status code: {resp.status_code},\nNext page: {next_url}") 
            return next_url
    
    def send_messages(self, url):
        messages = ["Hello there", "How are you?", "What's up?", "Testing 1", "Testing 2", "Testing 3", "Testing 4", "Testing 5", "Bye", "Have a nice day!"]
        for msg in messages:
            time.sleep(5, 10)
            data = {"text": msg}
            response = self.client.get(url, json=data, name="SendMessage")
            print(f"Sent message: {msg}, status: {response.status_code}")

    def str_random_choice(self, min=1, max=7):
        return str(random.randint(min, max))


    def on_start(self):
        session = self.user.session  # Inherit attributes of HttpUser Class
        with self.client.get(session, catch_response=True, name="ConsentPageEnter") as resp:
        # print(resp.status_code)
            resp_url = resp.url  # get the URL of the response
            match = re.search(r'/p/([^/]+)', resp_url)
            if match:
                self.p_id = match.group(1)
            else:
                self.p_id = "No matched p_id."

    @task
    def run_test(self):
        # Enter consent page
        # Transfer to on_start()
        p_id = self.p_id
        time.sleep(5)
        
        # Enter WelcomePage
        #Click Yes button (The same as the get method, but the latter will not elicit changes in the server.)
        data = {
            "agreement": "True",
        }
        next_url = self.next_page("/p/" + p_id + "/introduction/ConsentPage/1", data=data, name="ConsentPageSubmit") 
        # self.client.get("/p/" + p_id + "/introduction/WelcomePage/2", name="WelcomePage")
        time.sleep(random.randint(5, 10))

        # Enter task1/Priming
        data = {
            "prolificID": "test1234567812345678test",
            "avatar": "avatar/fox.png", # fox as avatar
            "nickname": "test_bot",
        }
        next_url = self.next_page(next_url, data=data, name="WelcomePageSubmit")
        time.sleep(random.randint(10, 20))
        

        # Enter task1 instruct
        data = {
            "primingText": "This is a test priming text." * 3,
        }
        next_url = self.next_page(next_url, data=data, name="Task1PrimingSubmit")
        time.sleep(5)

        # Enter waiting page 1
        next_url = self.next_page(next_url, name="Task1ChatInstructSubmit")
        time.sleep(15)  # Waiting for the pairing and capture the url of pairing success page
        next_url = self.next_page(next_url, name="WaitingPage1Submit")
        # pairing success （Don't need to wait for the pairing when using http requets)
        chat_url = self.next_page(next_url, name="Chat1PairingSuccess")
        logging.info(f"Chat1 url: {chat_url}")

        # Chat in task1
        self.send_messages(chat_url)  # Send 5 consecutive messages
        time.sleep(5)


        # Enter task2 instruction
        next_url = self.next_page(chat_url, name="ChatPage1Submit")
        time.sleep(5)

        # Enter waiting page 2
        next_url = self.next_page(next_url, name="Task2ChatInstructSubmit")
        time.sleep(15)  # Waiting for the pairing and capture the url of pairing success page
        next_url = self.next_page(next_url, name="WaitingPage2Submit")
        # pairing success
        chat_url = self.next_page(next_url, name="Chat2PairingSuccess")
        logging.info(f"Chat2 url: {chat_url}")

        # Chat in task2
        self.send_messages(chat_url)  # Send 5 consecutive messages
        time.sleep(5)

        # Enter survey prompt
        next_url = self.next_page(chat_url, name="ChatPage2Submit")
        time.sleep(random.randint(3, 5))

        # Enter survey pages
        logging.info(f"Survey prompt page: {next_url}")
        next_url = self.next_page(next_url, name="SurveyPromptSubmit")
        logging.info(f"Survey page 1: {next_url}")
        # Survey page 1
        data = {
            "senA_1": self.str_random_choice(),
            "senA_2": self.str_random_choice(),
            "senA_3": self.str_random_choice(),
            "senA_4": self.str_random_choice(),

            "feeH_1": self.str_random_choice(),
            "feeH_2": self.str_random_choice(),
            "feeH_3": self.str_random_choice(),
            "feeH_4": self.str_random_choice(),

            "CE_1": self.str_random_choice(),
            "CE_2": self.str_random_choice(),
            "CE_3": self.str_random_choice(),
            "CE_4": self.str_random_choice(),
        }
        time.sleep(random.randint(20, 30))
        next_url = self.next_page(next_url, data=data, name="SurveyPage1Submit")

        # Survey page 2
        data = {
            "AIU": self.str_random_choice(),

            "AIL_1": self.str_random_choice(),
            "AIL_2": self.str_random_choice(),
            "AIL_3": self.str_random_choice(),
            "AIL_4": self.str_random_choice(),

            "partner_label": "I don't know",
        }
        time.sleep(random.randint(15, 25))
        next_url = self.next_page(next_url, data=data, name="SurveyPage2Submit")
        
        # Survey page 3: Demographics
        data = {
            "age": "20",
            "gender": "Something else",
            "education": "Other",
            "race": "Other",
            "partisanship": "Other",
            "rlg_1": self.str_random_choice(),
            "rlg_2": self.str_random_choice(),
            "rlg_3": self.str_random_choice(),
            "rlg_4": self.str_random_choice(),
        }
        time.sleep(random.randint(20, 30))
        next_url = self.next_page(next_url, data=data, name="SurveyPage3Submit")

        # End: Payment Information
        time.sleep(5)
        # stop the user (necessary when using TaskSet)
        self.interrupt()

class SimulatedUser(HttpUser):
    host = "https://conversation-experiment.onrender.com"
    session = "/join/bazugujo"
    wait_time = constant(1)  # or between(1, 5): wait 1-5 seconds after each task
    # wait_time = constant_throughput(1) # 1 task (not request) per second
    tasks = [UserTask]

    # def on_start(self):


# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    logging.info("Start testing...")
    run_single_user(SimulatedUser)
    logging.info("Finish testing...")

