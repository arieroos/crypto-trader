import os
import hashlib
import hmac
import time

import orjson
import requests

import extra_math

URL = "https://api.valr.com"
VERSION = "/v1"

previous_signatures = set()


# As copied from VALR API example
def gen_signature(api_key_secret, timestamp, verb, path, body=""):
    """
    Signs the request payload using the api key secret
    api_key_secret - the api key secret
    timestamp - the unix timestamp of this request e.g. int(time.time()*1000)
    verb - Http verb - GET, POST, PUT or DELETE
    path - path excluding host name, e.g. '/v1/withdraw
    body - http request body as a string, optional
    """
    payload = "{}{}{}{}".format(timestamp, verb.upper(), path, body)
    message = bytearray(payload, 'utf-8')
    signature = hmac.new(bytearray(api_key_secret, 'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
    return signature


def gen_headers(method, path, body=""):
    server_time_json = requests.get(f"{URL}{VERSION}/public/time").json()

    timestamp = server_time_json["epochTime"] * 1000
    signature = gen_signature(os.environ["VALR_API_SECRET"], timestamp, method, path, body)
    while signature in previous_signatures:
        timestamp += 1
        signature = gen_signature(os.environ["VALR_API_SECRET"], timestamp, method, path, body)
    previous_signatures.add(signature)

    headers = {
        "X-VALR-API-KEY": os.environ["VALR_API_KEY"],
        "X-VALR-SIGNATURE": signature,
        "X-VALR-TIMESTAMP": str(timestamp),
    }
    if len(body) > 0:
        headers["Content-Type"] = "application/json"
    return headers


def check_response(resp: requests.Response):
    if resp.status_code > 400:
        raise Exception(f"Request {resp.request.url} failed with {resp.status_code}.\nBody: {resp.text}")


def market_summary():
    response = requests.get(f"{URL}{VERSION}/public/BTCZAR/marketsummary")
    check_response(response)
    return response.json()


def balances():
    path = f"{VERSION}/account/balances"
    headers = gen_headers("GET", path)
    response = requests.get(f"{URL}{path}", headers=headers)
    check_response(response)
    return response.json()


def balance(currency) -> float:
    b_list = balances()
    for b in b_list:
        if b['currency'] == currency:
            return float(b['available'])


def order_summary(oid: str) -> dict:
    path = f"{VERSION}/orders/history/summary/orderid/{oid}"
    headers = gen_headers("GET", path)
    resp = requests.get(url=f"{URL}{path}", headers=headers)
    return orjson.loads(resp.text)


def market_order_req(body):
    body_str = orjson.dumps(body).decode("utf-8")
    path = f"{VERSION}/orders/market"
    headers = gen_headers("POST", path, body_str)

    resp = requests.post(url=f"{URL}{path}", data=body_str, headers=headers)
    check_response(resp)
    try:
        order_id = orjson.loads(resp.text)["id"]
    except KeyError:
        raise Exception(orjson.loads(resp.text)["message"])
    time.sleep(1)  # allow order to be filled

    o_sum = order_summary(order_id)
    failure = o_sum["failedReason"]
    if len(failure) > 0:
        raise Exception(f"Order failed: {failure}")
    return float(o_sum["averagePrice"])


def buy_at_market():
    amt = balance("ZAR")
    if amt == 0:
        raise Exception("Trying to buy 0 ZAR of bitcoin?")
    print(f"Buying at market for R{amt}")

    amt = extra_math.floor_n(amt, 2)
    body = {
        "side": "BUY",
        "quoteAmount": f"{amt:.2f}",
        "pair": "BTCZAR",
    }
    return market_order_req(body)


def sell_at_market():
    amt = balance("BTC")
    if amt == 0:
        raise Exception("Trying to sell 0 bitcoin?")
    print(f"Selling {amt} BTC at market")

    amt = extra_math.floor_n(amt, 8)
    body = {
        "side": "SELL",
        "baseAmount": f"{amt:.8f}",
        "pair": "BTCZAR",
    }
    return market_order_req(body)


def buy_order(price: int) -> str:
    qty = balance("ZAR") / price
    if qty == 0:
        raise Exception("Trying to buy 0 bitcoin?")

    qty = extra_math.floor_n(qty, 8)
    body = {
        "side": "BUY",
        "quantity": f"{qty:.8f}",
        "price": str(price),
        "pair": "BTCZAR",
    }
    body_str = orjson.dumps(body).decode('utf-8')
    path = f"{VERSION}/orders/limit"
    headers = gen_headers("POST", path, body_str)

    resp = requests.post(url=f"{URL}{path}", data=body_str, headers=headers)
    check_response(resp)
    try:
        return resp.json()["id"]
    except KeyError:
        raise Exception(orjson.loads(resp.text)["message"])


def order_placed(oid: str) -> bool:
    return not order_summary(oid).get("failedReason", "")


def lowest_ask() -> float:
    path = f"{VERSION}/marketdata/BTCZAR/orderbook"
    headers = gen_headers("GET", path)
    resp = requests.get(f'{URL}{path}', headers=headers)

    asks = orjson.loads(resp.text)["Asks"]
    if len(asks) == 0:
        print("No ASKS returned from VALR")
        raise Exception()

    # According to VALR spec, asks[0] should be the lowest ask, but I do not trust that enough to not check
    return min([float(ask["price"]) for ask in asks])


def close_order(oid: str):
    body = {
        "orderId": oid,
        "pair": "BTCZAR",
    }
    body_str = orjson.dumps(body).decode("utf-8")
    path = f"{VERSION}/orders/order"
    headers = gen_headers("DELETE", path, body_str)
    resp = requests.delete(f"{URL}{path}", data=body_str, headers=headers)
    check_response(resp)


def get_open_orders():
    path = f"{VERSION}/orders/open"
    headers = gen_headers("GET", path)
    resp = requests.get(f"{URL}{path}", headers=headers)
    return orjson.loads(resp.text)


def close_open_buys():
    for order in get_open_orders():
        if order["side"].upper() == "BUY":
            print(f"Found order to close: {order['orderId']}")
            close_order(order["orderId"])


if __name__ == "__main__":
    print("MARKET SUMMARY")
    print(market_summary())
    print()
    print("BALANCES")
    print(balances())
    print()
    print("BTC BALANCE")
    print(f'{balance("BTC"):.8f}')
    print()
    print("OPEN ORDERS")
    print(get_open_orders())
    print()

    import sys
    if "test-market-sell-buy" in sys.argv:
        print("SELLING AT AT MARKET")
        p = sell_at_market()
        print(f"sold at {p}")
        print("BUYING AT MARKET")
        p = buy_at_market()
        print(f'bought at {p}')

    if "test-order-closing" in sys.argv:
        print("CLOSING ORDERS")
        close_open_buys()
