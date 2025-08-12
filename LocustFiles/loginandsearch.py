from locust import HttpUser, between, SequentialTaskSet
from LocustFiles.UserLogin import UserLogin
from LocustFiles.UserSearch import UserSearch

class LoginThenSearch(SequentialTaskSet):
    tasks = [UserLogin, UserSearch]  # Will run UserLogin first, then UserSearch

class MyLoadTest(HttpUser):
    host = "https://beta.twpn.com"
    wait_time = between(1, 2)
    tasks = [LoginThenSearch]


