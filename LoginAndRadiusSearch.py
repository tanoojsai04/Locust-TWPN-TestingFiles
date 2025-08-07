from locust import HttpUser, task, between, SequentialTaskSet, constant
from readtestdata import CsvRead
import re

class WebsiteUser(SequentialTaskSet):
    wait_time = between(1, 3)  # Simulates user wait time between tasks

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
                    userId = re.search(r'"userId"\s*:\s*"([a-f0-9-]+)"', response.text)                #Extracting the UserId
                    access_token = re.search(r'"access_token"\s*:\s*"([^"]+)"', response.text)         #Extracting the access_token
                    refresh_token = re.search(r'"refresh_token"\s*:\s*"([^"]+)"', response.text)       #Extracting the refresh _token
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
            "Cookie":f"{self.access_token}",
            "Accept": "*/*",
            "Connection": "keep-alive"
        }

        self.client.cookies.set("access_token", self.access_token)

        url=f"/api/twpn/property/radius-search?userId={self.userId}&preference=false&unit=km&limit=30&page=1&sort=LowestPrice&type=Sale&radius=5&lng=79.808708&lat=11.942923"

        with self.client.get(url, headers=headers, name = "RadiusSearch", catch_response=True) as response:
            print(f"Executing search with userId={self.userId} and token={self.access_token}")
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Search failed,{response.status_code} - {response.text}")

class MyLoadTest(HttpUser):
    host = "https://beta.twpn.com"
    tasks = [WebsiteUser]