#!/usr/bin/env python

import os
import json
import redis
from flask import Flask
from flask import request
from linkextractor import extract_links

app = Flask(__name__)


import time
import redis
import os

def connect_redis():
    url = os.getenv("REDIS_URL", "redis://localhost:6379")
    for i in range(10):
        try:
            conn = redis.from_url(url)
            conn.ping()
            print("✅ Conectado ao Redis")
            return conn
        except redis.ConnectionError:
            print(f"❌ Redis não disponível, tentativa {i+1}/10...")
            time.sleep(3)
    raise Exception("Não foi possível conectar ao Redis após 10 tentativas.")

redis_conn = connect_redis()
    


@app.route("/")
def index():
    return "Usage: http://<hostname>[:<prt>]/api/<url>"

@app.route("/api/<path:url>")
def api(url):
    qs = request.query_string.decode("utf-8")
    if qs != "":
        url += "?" + qs

    jsonlinks = redis_conn.get(url)
    if not jsonlinks:
        links = extract_links(url)
        jsonlinks = json.dumps(links, indent=2)
        redis_conn.set(url, jsonlinks)

    response = app.response_class(
        status=200,
        mimetype="application/json",
        response=jsonlinks
    )

    return response

app.run(host="0.0.0.0")
