from readtestdata import CsvRead
from locust import task, TaskSet
from token_handler import TokenHandler
from logger import log_info, log_error

class UserSearch(TaskSet):

    run_only = ["search_basic", "search_radius","search_complete","search_global","search_advanced_dropdown"]

    def __init__(self, parent):
        super().__init__(parent)
        self.refresh_token = None
        self.access_token = None
        self.userId = None
        self.common_headers = ""

    def on_start(self):
        # ✅ Retrieve tokens from TokenHandler
        self.userId = TokenHandler.get_user_id()
        self.access_token = TokenHandler.get_access_token()
        self.refresh_token = TokenHandler.get_refresh_token()

        self.common_headers = {
            "userid": f"{self.userId}",
            "Cookie": f"access_token={self.access_token}; refresh_token={self.refresh_token}",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Authorization": f"Bearer {self.access_token}"
        }
        self.client.cookies.set("access_token", self.access_token)
        self.client.cookies.set("refresh_token", self.refresh_token)

        print(f"✅ Allowed tasks: {self.run_only}")

    @task(30)
    def search_basic(self):
        if "search_basic" not in self.run_only:
            return  # ❌ Skip if not in allowed list

        test_data = CsvRead("../TestDataFiles/twpntestfileSheet1.csv").read()

        data = {

            "type": test_data['type'],
            "country": test_data['country'],
            "sort": test_data['sort']
        }

        url="/api/twpn/property/basic-search?page=1&limit=30&type=Sale&query=Florida"

        with self.client.get(url=url,headers=self.common_headers, data=data, name="Web-BasicSearch", catch_response=True) as response:
            if response.status_code == 200 and "OK" in response.text:
                log_info(f"Search successful, {response.status_code}")
                response.success()
            else:
                log_error(f"Search failed: {response.status_code} - {response.text}")

    @task(40)
    def search_radius(self):
        if "search_radius" not in self.run_only:
            return

        url = f"/api/twpn/property/radius-search?userId={self.userId}&preference=false&unit=km&limit=30&page=1&&sort=LowestPrice&type=Sale&radius=5&lng=79.808708&lat=11.942923"

        with self.client.get(url=url, headers=self.common_headers, name="RadiusSearch-propertySnap",  catch_response=True) as response:
            print(f"Executing search with userId={self.userId} and token={self.access_token}")
            if response.status_code == 200:
                response.success()
                log_info(f"Radius Search successful, {response.text}")
            else:
                log_error(f"Search failed,{response.status_code} - {response.text}")

    @task(30)
    def search_complete(self):
        if "search_complete" not in self.run_only:
            return

        test_data = CsvRead("../TestDataFiles/twpntestfileSheet1.csv").read()

        data = {

            "type": test_data['type'],
            "country": test_data['country'],
            "sort": test_data['sort']
        }

        params={
            "searchTerm" : "wood"
        }

        url = f"/api/twpn/property/auto-complete"

        with self.client.get(url=url, headers=self.common_headers, name="Auto-complete-search", data=data, params=params, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                log_info(f"auto-complete successful, {response.text}")
            else:
                response.failure(f"Search failed,{response.status_code} - {response.text}")

    @task(30)
    def search_global(self):
        if "search_global" not in self.run_only:
            return

        test_data = CsvRead("../TestDataFiles/twpntestfileSheet1.csv").read()

        params = {

            "type": test_data['type'],
            "country": test_data['country'],
            "sort": test_data['sort']
        }

        url = f"/api/twpn/property/global-search?page=150&limit=10&preference=false&lat=53.798053&lng=-1.693632&query=Jamaica&userId={self.userId}"

        with self.client.get(url=url, headers=self.common_headers, name="App-global-search", params=params,
                             catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                log_info(f"global search successful, {response.text}")
            else:
                response.failure(f"Search failed,{response.status_code} - {response.text}")

    @task(30)
    def search_advanced_dropdown(self):
        if "search_advanced_dropdown" not in self.run_only:
            return

        test_data = CsvRead("../TestDataFiles/twpntestfileSheet1.csv").read()

        data = {

            "type": test_data['type'],
            "country": test_data['country'],
            "sort": test_data['sort']
        }

        url = f"/api/twpn/property/advanced-search-dropdown"

        with self.client.get(url=url, headers=self.common_headers, name="web-advanced-search-dropdown", data=data,
                             catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                log_info(f"adv_sear_dropdown, {response.text}")
            else:
                response.failure(f"Search failed,{response.status_code} - {response.text}")
