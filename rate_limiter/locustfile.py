from locust import HttpUser, task

class Limited_User(HttpUser):
    @task
    def limit_user(self):
        self.client.get("/limited")
        # self.client.get("/world")