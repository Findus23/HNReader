import json
import subprocess
from pathlib import Path

from redis import Redis
from requests import Session


class Reader:
    def __init__(self, url: str, requests_session: Session, redis: Redis):
        self.url = url
        self.s = requests_session
        self.r = redis

    def readable_html(self):
        php_file = Path(__file__).parent / "reader.php"
        output = subprocess.run(["php", str(php_file)], input=self.url.encode(), capture_output=True)
        data = json.loads(output.stdout.decode())
        del data["headers"]
        del data["summary"]
        return json.dumps(data)
