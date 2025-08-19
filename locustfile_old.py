import time
import random
import re
from locust import HttpUser, task, between, run_single_user

def arb_time():
    return random.uniform(3, 30)

class Emo_H2B_User(HttpUser):
    host = "https://chat-experim-master-bwl9y41oqg.herokuapp.com"
    wait_time = between(1, 5)  # wait 1-5 seconds after each task
    weight = 1

    @task
    def lets_chat(self):
        with self.client.get("/room/Room_1_pilot1", catch_response=True, name="ConsentPage") as resp:
            # print(resp.status_code)
            resp_url = resp.url  # get the URL of the response
            match = re.search(r'/p/([^/]+)', resp_url)
            if match:
                p_id = match.group(1)
            else:
                p_id = "No matched p_id."
            # pass
        
        self.client.get("/p/" + p_id + "/introduction/WelcomePage/2", name="WelcomePage")
        time.sleep(arb_time())

        # Enter task1
        self.client.get("/p/" + p_id + "/task1/taskPriming/3", name="Task1/Priming")
        time.sleep(arb_time())

        self.client.get("/p/" + p_id + "/task1/chatInstruct/4", name="Task1/ChatInstruct")
        time.sleep(arb_time())

        # Waiting for the pairing
        self.client.get("/p/" + p_id + "/chat_B/MyWaitPage/9", name="chat_B/MyWaitPage")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/chat_B/pairingSuc/10", name="chat_B/pairingSuc")
        time.sleep(arb_time())

        # Chat in task1
        self.client.get("/p/" + p_id + "/chat_B/chatEmo/11", name="chat_B/chatEmo")
        time.sleep(arb_time())
        # self.client.get("/p/" + p_id + "/chat_B/chatFun/12", name="chat_B/chatFun")
        # time.sleep(30)
        for i in range(5):
            self.client.post("/p/" + p_id + "/chat_B/chatEmo/11", {"data": "test1"}, name="chat_B/chatEmo")
            time.sleep(5)

        # Enter task2
        self.client.get("/p/" + p_id + "/task2/chatInstruct_emo_human/13", name="task2/chatInstruct_emo_human")
        time.sleep(arb_time())

        # Waiting for the pairing
        self.client.get("/p/" + p_id + "/chat_H2r/MyWaitPage/15", name="chat_H2r/MyWaitPage")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/chat_H2r/pairingSuc/16", name="chat_B/pairingSuc")
        time.sleep(arb_time())

        # Chat in task2
        self.client.get("/p/" + p_id + "/chat_H2r/chatEmo/17", name="chat_H2r/chatEmo")
        time.sleep(arb_time())
        # self.client.get("/p/" + p_id + "/chat_H2r/chatFun/18", name="chat_H2r/chatFun")
        # time.sleep(30)
        for i in range(5):
            self.client.post("/p/" + p_id + "/chat_H2r/chatEmo/17", {"data": "test1"}, name="chat_H2r/chatEmo")
            time.sleep(5)

        # Survey
        self.client.get("/p/" + p_id + "/survey/Prompt/22", name="survey/Prompt")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/VariablePageA/23", name="survey/VariablePageA")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/VariablePageB/24", name="survey/VariablePageB")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/Demographics/25", name="survey/Demographics")
        time.sleep(arb_time())

        # End
        self.client.get("/p/" + p_id + "/payment_info/PaymentInfo/26", name="PaymentInfo")
        time.sleep(arb_time())
        pass


class Emo_H2H_User(HttpUser):
    host = "https://chat-experim-master-bwl9y41oqg.herokuapp.com"
    wait_time = between(1, 5)  # wait 1-5 seconds after each task
    weight = 1

    @task
    def lets_chat(self):
        with self.client.get("/room/Room_1_pilot1", catch_response=True, name="ConsentPage") as resp:
            # print(resp.status_code)
            resp_url = resp.url  # get the URL of the response
            match = re.search(r'/p/([^/]+)', resp_url)
            if match:
                p_id = match.group(1)
            else:
                p_id = "No matched p_id."
            # pass
        
        self.client.get("/p/" + p_id + "/introduction/WelcomePage/2", name="WelcomePage")
        time.sleep(arb_time())

        # Enter task1
        self.client.get("/p/" + p_id + "/task1/taskPriming/3", name="Task1/Priming")
        time.sleep(arb_time())

        self.client.get("/p/" + p_id + "/task1/chatInstruct/4", name="Task1/ChatInstruct")
        time.sleep(arb_time())

        # Waiting for the pairing
        self.client.get("/p/" + p_id + "/chat_H/MyWaitPage/5", name="chat_H/MyWaitPage")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/chat_H/pairingSuc/6", name="chat_H/pairingSuc")
        time.sleep(arb_time())

        # Chat in task1
        self.client.get("/p/" + p_id + "/chat_H/chatEmo/7", name="chat_H/chatEmo")
        time.sleep(arb_time())
        for i in range(5):
            self.client.post("/p/" + p_id + "/chat_H/chatEmo/7", {"data": "test"}, name="chat_H/chatEmo")
            time.sleep(5)

        # Enter task2
        self.client.get("/p/" + p_id + "/task2/chatInstruct_emo_human/13", name="task2/chatInstruct_emo_human")
        time.sleep(arb_time())

        # Waiting for the pairing
        self.client.get("/p/" + p_id + "/chat_H2r/MyWaitPage/15", name="chat_H2r/MyWaitPage")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/chat_H2r/pairingSuc/16", name="chat_B/pairingSuc")
        time.sleep(arb_time())

        # Chat in task2
        self.client.get("/p/" + p_id + "/chat_H2r/chatEmo/17", name="chat_H2r/chatEmo")
        time.sleep(arb_time())
        # self.client.get("/p/" + p_id + "/chat_H2r/chatFun/18", name="chat_H2r/chatFun")
        # time.sleep(30)
        for i in range(5):
            self.client.post("/p/" + p_id + "/chat_H2r/chatEmo/17", {"data": "test"}, name="chat_H2r/chatEmo")
            time.sleep(5)

        # Survey
        self.client.get("/p/" + p_id + "/survey/Prompt/22", name="survey/Prompt")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/VariablePageA/23", name="survey/VariablePageA")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/VariablePageB/24", name="survey/VariablePageB")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/Demographics/25", name="survey/Demographics")
        time.sleep(arb_time())

        # End
        self.client.get("/p/" + p_id + "/payment_info/PaymentInfo/26", name="PaymentInfo")
        time.sleep(arb_time())
        pass


class Fun_H2B_User(HttpUser):
    host = "https://chat-experim-master-bwl9y41oqg.herokuapp.com"
    wait_time = between(1, 5)  # wait 1-5 seconds after each task
    weight = 1

    @task
    def lets_chat(self):
        with self.client.get("/room/Room_1_pilot1", catch_response=True, name="ConsentPage") as resp:
            # print(resp.status_code)
            resp_url = resp.url  # get the URL of the response
            match = re.search(r'/p/([^/]+)', resp_url)
            if match:
                p_id = match.group(1)
            else:
                p_id = "No matched p_id."
            # pass
        
        self.client.get("/p/" + p_id + "/introduction/WelcomePage/2", name="WelcomePage")
        time.sleep(arb_time())

        # Enter task1
        self.client.get("/p/" + p_id + "/task1/taskPriming/3", name="Task1/Priming")
        time.sleep(arb_time())

        self.client.get("/p/" + p_id + "/task1/chatInstruct/4", name="Task1/ChatInstruct")
        time.sleep(arb_time())

        # Waiting for the pairing
        self.client.get("/p/" + p_id + "/chat_B/MyWaitPage/9", name="chat_B/MyWaitPage")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/chat_B/pairingSuc/10", name="chat_B/pairingSuc")
        time.sleep(arb_time())

        # Chat in task1
        self.client.get("/p/" + p_id + "/chat_B/chatFun/12", name="chat_B/chatFun")
        time.sleep(arb_time())
        for i in range(5):
            self.client.post("/p/" + p_id + "/chat_B/chatFun/12", {"data": "test"}, name="chat_B/chatFun")
            time.sleep(5)

        # Enter task2
        self.client.get("/p/" + p_id + "/task2/chatInstruct_fun_human/14", name="task2/chatInstruct_fun_human")
        time.sleep(arb_time())

        # Waiting for the pairing
        self.client.get("/p/" + p_id + "/chat_H2r/MyWaitPage/15", name="chat_H2r/MyWaitPage")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/chat_H2r/pairingSuc/16", name="chat_B/pairingSuc")
        time.sleep(arb_time())

        # Chat in task2
        self.client.get("/p/" + p_id + "/chat_H2r/chatFun/18", name="chat_H2r/chatFun")
        time.sleep(arb_time())
        for i in range(5):
            self.client.post("/p/" + p_id + "/chat_H2r/chatFun/18", {"data": "test"}, name="chat_H2r/chatFun")
            time.sleep(5)


        # Survey
        self.client.get("/p/" + p_id + "/survey/Prompt/22", name="survey/Prompt")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/VariablePageA/23", name="survey/VariablePageA")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/VariablePageB/24", name="survey/VariablePageB")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/Demographics/25", name="survey/Demographics")
        time.sleep(arb_time())

        # End
        self.client.get("/p/" + p_id + "/payment_info/PaymentInfo/26", name="PaymentInfo")
        time.sleep(arb_time())
        pass

class Fun_H2H_User(HttpUser):
    host = "https://chat-experim-master-bwl9y41oqg.herokuapp.com"
    wait_time = between(1, 5)  # wait 1-5 seconds after each task
    weight = 1

    @task
    def lets_chat(self):
        with self.client.get("/room/Room_1_pilot1", catch_response=True, name="ConsentPage") as resp:
            # print(resp.status_code)
            resp_url = resp.url  # get the URL of the response
            match = re.search(r'/p/([^/]+)', resp_url)
            if match:
                p_id = match.group(1)
            else:
                p_id = "No matched p_id."
            # pass
        
        self.client.get("/p/" + p_id + "/introduction/WelcomePage/2", name="WelcomePage")
        time.sleep(arb_time())

        # Enter task1
        self.client.get("/p/" + p_id + "/task1/taskPriming/3", name="Task1/Priming")
        time.sleep(arb_time())

        self.client.get("/p/" + p_id + "/task1/chatInstruct/4", name="Task1/ChatInstruct")
        time.sleep(arb_time())

        # Waiting for the pairing
        self.client.get("/p/" + p_id + "/chat_H/MyWaitPage/5", name="chat_H/MyWaitPage")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/chat_H/pairingSuc/6", name="chat_H/pairingSuc")
        time.sleep(arb_time())

        # Chat in task1
        self.client.get("/p/" + p_id + "/chat_H/chatFun/8", name="chat_H/chatFun")
        time.sleep(arb_time())
        for i in range(5):
            self.client.post("/p/" + p_id + "/chat_H/chatFun/8", {"data": "test"}, name="chat_H/chatFun")
            time.sleep(5)


        # Enter task2
        self.client.get("/p/" + p_id + "/task2/chatInstruct_fun_human/14", name="task2/chatInstruct_fun_human")
        time.sleep(arb_time())

        # Waiting for the pairing
        self.client.get("/p/" + p_id + "/chat_H2r/MyWaitPage/15", name="chat_H2r/MyWaitPage")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/chat_H2r/pairingSuc/16", name="chat_B/pairingSuc")
        time.sleep(arb_time())

        # Chat in task2
        self.client.get("/p/" + p_id + "/chat_H2r/chatFun/18", name="chat_H2r/chatFun")
        time.sleep(arb_time())
        for i in range(5):
            self.client.post("/p/" + p_id + "/chat_H2r/chatFun/18", {"data": "test"}, name="chat_H2r/chatFun")
            time.sleep(5)

        # Survey
        self.client.get("/p/" + p_id + "/survey/Prompt/22", name="survey/Prompt")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/VariablePageA/23", name="survey/VariablePageA")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/VariablePageB/24", name="survey/VariablePageB")
        time.sleep(arb_time())
        self.client.get("/p/" + p_id + "/survey/Demographics/25", name="survey/Demographics")
        time.sleep(arb_time())

        # End
        self.client.get("/p/" + p_id + "/payment_info/PaymentInfo/26", name="PaymentInfo")
        time.sleep(arb_time())
        pass

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})
    #     with self.client.get("/room/Room_1_pilot1") as response:
    #         print(response)


# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(Fun_H2H_User)

