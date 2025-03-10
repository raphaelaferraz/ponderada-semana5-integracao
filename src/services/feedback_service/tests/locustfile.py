from locust import HttpUser, task, between

class FeedbackUser(HttpUser):
    wait_time = between(1, 3)  

    @task
    def post_feedback(self):
        payload = {
            "motoboy_id": 123,
            "response": "O aplicativo está com atraso e precisa de melhorias."
        }
        self.client.post("/feedback/", json=payload)

    @task
    def get_feedbacks(self):
        self.client.get("/feedbacks/")
