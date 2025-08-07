import re
from readtestdata import CsvRead
from locust import HttpUser, task, between, TaskSet


class MyUser(TaskSet):
    wait_time = between(1, 2)

    def __init__(self, parent):
        super().__init__(parent)
        self.userId = ""
        self.access_token = ""
        self.refresh_token = ""

    def on_start(self):
        """Login and store token before executing other tasks"""
        self.login()

    @task
    def login(self):
        # Modify with your actual login payload
        test_data = CsvRead("TWPNusers.csv").read()

        data = {

            "email": test_data['email'],
            "password": test_data['password']
        }

        with self.client.post("/api/auth/login", json=data, catch_response=True) as response:

            if response.status_code == 200:
                try:
                    userId = re.search(r'"userId"\s*:\s*"([a-f0-9-]+)"', response.text)  # Extracting the UserId
                    access_token = re.search(r'"access_token"\s*:\s*"([^"]+)"',response.text)  # Extracting the access_token
                    refresh_token = re.search(r'"refresh_token"\s*:\s*"([^"]+)"',response.text)  # Extracting the refresh _token
                    self.userId = userId.group(1)
                    self.access_token = access_token.group(1)
                    self.refresh_token = refresh_token.group(1)
                    print(userId.group(1))
                except AttributeError:
                    self.userId = ""
                    self.access_token = ""
                    self.refresh_token = ""
                    response.failure("Failed to extract tokens")

            else:
                response.failure(f"{response.status_code}")


    @task
    def search(self):

        headers = {

            "userid":self.userId
        }


        with self.client.get("/api/twpn/property/basic-search?page=1&limit=30&type=Sale&query=Florida", headers=headers, name="Basic Search", catch_response=True) as response:
            if response.status_code == 200 and "OK" in response.text:
                print("Search successful")
                response.success()
            else:
                response.failure(f"Search failed: {response.status_code} - {response.text}")

        self.client.cookies.set("access_token", self.access_token)


class MyLoadTest(HttpUser):
    host = "https://beta.twpn.com"
    tasks = [MyUser]