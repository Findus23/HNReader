import asyncio
import json

from aiohttp import ClientSession
from redis import Redis

API_BASEURL = "https://hacker-news.firebaseio.com/v0/"


class HNClient:
    def __init__(self, session: ClientSession, redis: Redis):
        self.s = session
        self.r = redis

    async def get_item(self, item_id: int, remove_kids=True):
        key = f"hnclient_item_{item_id}"
        cache = self.r.get(key)
        if cache:
            return json.loads(cache)
        url = f"{API_BASEURL}item/{item_id}.json"
        async with self.s.get(url) as response:
            response.raise_for_status()
            text = await response.text()
            item = json.loads(text)
        self.r.set(key, text, ex=60 * 15)
        if "kids" in item and remove_kids:
            del item["kids"]
        return item

    async def get_full_item(self, item_id: int):
        item = await self.get_item(item_id, remove_kids=False)
        if "kids" in item:
            tasks = []
            for kid in item["kids"]:
                task = asyncio.ensure_future(self.get_full_item(kid))
                tasks.append(task)

            kids = await asyncio.gather(*tasks)
            item["kids"] = kids
        return item

    async def get_stories(self, page: str, offset=0):
        limit = 25
        key = f"hnclient_stories_{page}_{offset}"
        cached = self.r.get(key)
        if cached:
            return json.loads(cached)
        url = f"{API_BASEURL}{page}.json"
        async with self.s.get(url) as response:
            response.raise_for_status()
            stories = await response.json()
            stories = stories[offset:limit + offset]
        tasks = []
        for id in stories:
            task = asyncio.ensure_future(self.get_item(id))
            tasks.append(task)

        full_stories = await asyncio.gather(*tasks)
        self.r.set(key, json.dumps(full_stories), ex=60 * 15)
        return full_stories
