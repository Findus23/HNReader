import requests
from flask import Flask, jsonify, make_response
from redis import Redis

from config import user_agent
from hnapi import HNClient
from reader import Reader

app = Flask(__name__)
r = Redis()
s = requests.session()
s.headers.update({'User-Agent': user_agent})

api = HNClient(s, r)


@app.route("/api/topstories")
def topstories():
    return jsonify(api.get_stories("topstories"))


@app.route("/api/item/<int:item_id>")
def item(item_id):
    return jsonify(api.get_full_item(item_id))


@app.route("/api/read/<int:item_id>")
def read(item_id):
    item = api.get_item(item_id)
    if "url" not in item:
        return "Url not found", 404
    key = f"hnclient_read_{item_id}"

    cache = r.get(key)
    if cache:
        response = make_response(cache)
    else:
        readable = Reader(item["url"], s, r)
        output = readable.readable_html()
        r.set(key, output, ex=60 * 60 * 24)
        response = make_response(output)
    response.headers["Content-Type"] = "application/json"
    return response
