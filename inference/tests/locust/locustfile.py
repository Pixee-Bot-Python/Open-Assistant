import string
import sys
import time
from pathlib import Path

from locust import HttpUser, between, task
import secrets

sys.path.append(str(Path(__file__).parent.parent.parent / "text-client"))
import text_client_utils as utils  # noqa: E402


class ChatUser(HttpUser):
    wait_time = between(1, 2)
    conversation_length = secrets.SystemRandom().randint(3, 20)
    time_to_respond = secrets.SystemRandom().randint(3, 5)  # for the user
    # model_config_name = "distilgpt2"
    model_config_name = "_lorem"

    @task
    def chat(self):
        client = utils.DebugClient(backend_url="", http_client=self.client)
        username = "".join(secrets.choice(string.ascii_lowercase) for _ in range(20))
        client.login(username)
        client.create_chat()

        for _ in range(self.conversation_length):
            for _ in client.send_message("hello", self.model_config_name):
                pass

            time.sleep(self.time_to_respond)
