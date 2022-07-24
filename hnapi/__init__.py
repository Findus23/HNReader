import asyncio
import json

from redis.asyncio.client import StrictRedis
from httpx import AsyncClient

API_BASEURL = "https://hacker-news.firebaseio.com/v0/"


class HNClient:
    def __init__(self, session: AsyncClient, redis: StrictRedis):
        self.s = session
        self.r = redis

    async def get_item(self, item_id: int, remove_kids=True):
        key = f"hnclient_item_{item_id}"
        cache = await self.r.get(key)
        if cache:
            return json.loads(cache)
        url = f"{API_BASEURL}item/{item_id}.json"
        response = await self.s.get(url)
        response.raise_for_status()
        item = json.loads(response.text)
        await self.r.set(key, response.text, ex=60 * 15)
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
        cached = await self.r.get(key)
        if cached:
            return json.loads(cached)
        url = f"{API_BASEURL}{page}.json"
        response = await self.s.get(url)
        response.raise_for_status()
        stories = response.json()
        stories = stories[offset:limit + offset]
        tasks = []
        for id in stories:
            task = asyncio.ensure_future(self.get_item(id))
            tasks.append(task)

        full_stories = await asyncio.gather(*tasks)
        await self.r.set(key, json.dumps(full_stories), ex=60 * 15)
        return full_stories
