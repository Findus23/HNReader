import aiohttp
from redis import Redis
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from config import debug
from hnapi import HNClient
from reader import Reader

conn = aiohttp.TCPConnector(ttl_dns_cache=60 * 10)
session = aiohttp.ClientSession(connector=conn)
r = Redis()
reader = Reader()

api = HNClient(session, r)


async def item(request: Request):
    item_id = request.path_params["item_id"]
    data = await api.get_full_item(item_id)
    return JSONResponse(data)


async def read(request: Request):
    item_id = request.path_params["item_id"]
    item = await api.get_item(item_id)
    if "url" not in item:
        return "Url not found", 404
    key = f"hnclient_read_{item_id}"

    cache = r.get(key)
    if cache:
        response = Response(cache)
    else:
        output = await reader.readable_html(item["url"])
        r.set(key, output, ex=60 * 60 * 24)
        response = Response(output)
    response.media_type = "application/json"
    return response


async def topstories(request: Request):
    data = await api.get_stories("topstories")
    return JSONResponse(data)


app = Starlette(debug=debug, routes=[
    Route('/api/item/{item_id:int}', item),
    Route('/api/read/{item_id:int}', read),
    Route('/api/topstories', topstories),
])

