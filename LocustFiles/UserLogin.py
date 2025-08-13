import re
import os
from readtestdata import CsvRead
from locust import task, TaskSet
from token_handler import TokenHandler


class UserLogin(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.userId=""
        self.access_token=""
        self.refresh_token=""

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_path_users = os.path.join(base_dir, "TestDataFiles", "TWPNusers.csv")

    def on_start(self):
        """Login and store token before executing other tasks"""
        self.login()

    @task
    def login(self):
        # Modify with your actual login payload
        test_data = CsvRead(self.csv_path_users).read()
        data = {

            "email": test_data['email'],
            "password": test_data['password']
        }

        with self.client.post("/api/auth/login", json=data, name = "Login", catch_response=True) as response:
            print("Login Successful", response.text)
            if response.status_code == 200:
                try:
                    userId = re.search(r'"userId"\s*:\s*"([a-f0-9-]+)"', response.text)  # Extracting the UserId
                    access_token = re.search(r'"access_token"\s*:\s*"([^"]+)"',response.text)  # Extracting the access_token
                    refresh_token = re.search(r'"refresh_token"\s*:\s*"([^"]+)"',response.text)  # Extracting the refresh _token

                    self.userId = userId.group(1)
                    self.access_token = access_token.group(1)
                    self.refresh_token = refresh_token.group(1)

                    # ✅ Store tokens globally
                    TokenHandler.set_tokens(self.access_token, self.refresh_token, self.userId)

                    print(f"login successful,{self.userId}")
                except AttributeError:
                    self.userId = ""
                    self.access_token = ""
                    self.refresh_token = ""
                    response.failure("Failed to extract tokens")

            else:
                response.failure(f"{response.status_code}")
        self.interrupt(reschedule=False)
