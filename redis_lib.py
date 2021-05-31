from datetime import datetime

import redis as redis


def gen_key(name: str) -> str:
    return f"cb:{name}"


def save_price(price):
    kn = datetime.now().strftime("%y-%m-%d:%H")
    key = gen_key(kn)

    r = redis.Redis()
    r.set(key, str(price))
