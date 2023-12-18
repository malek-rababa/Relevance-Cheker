from locust import HttpUser, task, between

class MyTaskSet(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        pass

    @task
    def check_relevance(self):
        tweet = "Sample tweet content"  # Replace with actual tweet content
        reply = "Sample reply content"  # Replace with actual reply content

        # Simulate form input
        payload = {"tweet": tweet, "reply": reply}

        # Send POST request
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.client.get("http://127.0.0.1:5000", data=payload, headers=headers)

        # Print response content for debugging
        print(response.content)

# Run Locust
# locust -f locustfile.py
