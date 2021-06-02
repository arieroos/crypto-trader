from datetime import datetime, timedelta

import redis


def gen_key(name: str) -> str:
    return f"cb:{name}"


def hour_key(t: datetime) -> str:
    return gen_key(t.strftime("%y-%m-%d:%H"))


def connection() -> redis.Redis:
    return redis.Redis()


def save_price(price: int):
    key = hour_key(datetime.now())

    r = connection()
    r.set(key, str(price))


def last_prices(n: int) -> list[int]:
    t = datetime.now()

    r = connection()
    res = []
    for _ in range(0, n):
        key = hour_key(t)
        p = r.get(key)
        if p is not None:
            res.append(int(p))

        t = t - timedelta(hours=1)

    return res


def save_trend(trend: str):
    connection().set(gen_key("trend"), trend)


def last_trend() -> str:
    return connection().get(gen_key("trend"))
