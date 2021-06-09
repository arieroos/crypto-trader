import os
import hashlib
import hmac

import orjson
import requests

URL = "https://api.valr.com"
VERSION = "/v1"


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
    secret = gen_signature(os.environ["VALR_API_SECRET"], timestamp, method, path, body)

    headers = {
        "X-VALR-API-KEY": os.environ["VALR_API_KEY"],
        "X-VALR-SIGNATURE": secret,
        "X-VALR-TIMESTAMP": str(timestamp),
    }
    if len(body) > 0:
        headers["Content-Type"] = "application/json"
    return headers


def market_summary():
    response = requests.get(f"{URL}{VERSION}/public/BTCZAR/marketsummary")
    return response.json()


def balances():
    path = f"{VERSION}/account/balances"
    headers = gen_headers("GET", path)
    response = requests.get(f"{URL}{path}", headers=headers)
    return response.json()


def balance(currency) -> float:
    b_list = balances()
    for b in b_list:
        if b['currency'] == currency:
            return float(b['available'])


def sell_at_market():
    amt = balance("BTC")
    body = {
        "side": "SELL",
        "amount": f"{amt:.8f}",
        "pair": "BTCZAR",
    }
    body_str = orjson.dumps(body).decode("utf-8")
    path = f"{VERSION}/orders/market"
    headers = gen_headers("POST", "", body_str)

    requests.post(url=f"{URL}{path}", data=body_str, headers=headers)


if __name__ == "__main__":
    print("MARKET SUMMARY")
    print(market_summary())
    print("BALANCES")
    print(balances())
    print("BTC BALANCE")
    print(f'{balance("BTC"):.8f}')
