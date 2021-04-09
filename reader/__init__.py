import asyncio
import json
from pathlib import Path


class Reader:
    async def readable_html(self, url: str):
        php_file = Path(__file__).parent / "reader.php"
        process = await asyncio.create_subprocess_exec(
            "php", str(php_file),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate(url.encode())
        data = json.loads(stdout.decode().strip())
        del data["headers"]
        del data["summary"]
        return json.dumps(data)
