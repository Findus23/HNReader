import aiohttp
from aredis import StrictRedis
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from config import debug, user_agent, redis_socket
from hnapi import HNClient
from reader import Reader

conn = aiohttp.TCPConnector(ttl_dns_cache=60 * 10)
session = aiohttp.ClientSession(connector=conn, headers={
    "User-Agent": user_agent
})
if redis_socket:
    r = StrictRedis(unix_socket_path=redis_socket)
else:
    r = StrictRedis()
reader = Reader()

api = HNClient(session, r)


async def item(request: Request):
    item_id = request.path_params["item_id"]
    data = await api.get_full_item(item_id)
    return JSONResponse(data)


async def read(request: Request):
    print(request.session)
    request.session.update({"a": "b"})
    item_id = request.path_params["item_id"]
    item = await api.get_item(item_id)
    if "url" not in item:
        return "Url not found", 404
    key = f"hnclient_read_{item_id}"

    cache = await r.get(key)
    if cache:
        response = Response(cache)
    else:
        output = await reader.readable_html(item["url"])
        await r.set(key, output, ex=60 * 60 * 24)
        response = Response(output)
    response.media_type = "application/json"
    return response


async def topstories(request: Request):
    offset = int(request.query_params.get("offset", 0))
    data = await api.get_stories("topstories", offset=offset)
    return JSONResponse(data)


app = Starlette(debug=debug, routes=[
    Route('/api/item/{item_id:int}', item),
    Route('/api/read/{item_id:int}', read),
    Route('/api/topstories', topstories),
])
