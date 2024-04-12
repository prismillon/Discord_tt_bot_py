import re
from motor.motor_asyncio import AsyncIOMotorClient
import os

import redis.asyncio
import redis

mongodb_url = os.environ.get("MONGODB_URL")
client = AsyncIOMotorClient(mongodb_url)
db = client["quaxly"]

redis_url = os.environ.get("REDIS_URL")
r = redis.asyncio.Redis(host=redis_url, port=6379, socket_keepalive=True)
rs = redis.Redis(host=redis_url, port=6379)
