import json
from dataclasses import dataclass
from typing import List

from redis import Redis
from requests import Session

API_BASEURL = "https://hacker-news.firebaseio.com/v0/"


@dataclass
class Item:
    id: int
    type: str
    by: str
    time: int
    url: str
    score: int
    title: str
    # parts: ??
    deleted: bool = None
    text: str = None  # HTML
    dead: bool = None
    parent: int = None
    poll: int = None
    kids: List[int] = None
    descendants: int = None


class HNClient:
    def __init__(self, requests_session: Session, redis: Redis):
        self.s = requests_session
        self.r = redis

    def get_item(self, item_id: int, remove_kids=True):
        key = f"hnclient_item_{item_id}"
        cache = self.r.get(key)
        if cache:
            return json.loads(cache)
        url = f"{API_BASEURL}item/{item_id}.json"
        response = self.s.get(url)
        response.raise_for_status()
        item = response.json()
        self.r.set(key, response.text, ex=60 * 15)
        if "kids" in item and remove_kids:
            del item["kids"]
        return item

    def get_full_item(self, item_id: int):
        item = self.get_item(item_id, remove_kids=False)
        if "kids" in item:
            kids = list(self.get_items_by_id(item["kids"], full=True))
            item["kids"] = kids
        return item

    def get_items_by_id(self, ids: List[int], full=False):
        for id in ids:
            if full:
                yield self.get_full_item(id)
            else:
                yield self.get_item(id)

    def get_stories(self, page: str, limit=25, offset=0):
        key = f"hnclient_stories_{page}_{limit}"
        cached = self.r.get(key)
        if cached:
            return json.loads(cached)
        url = f"{API_BASEURL}{page}.json"
        response = self.s.get(url)
        response.raise_for_status()
        stories = response.json()[offset:limit]
        full_stories = list(self.get_items_by_id(stories))
        self.r.set(key, json.dumps(full_stories), ex=60 * 15)
        return full_stories
