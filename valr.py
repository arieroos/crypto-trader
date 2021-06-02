import os
import hashlib
import hmac

import requests


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


def gen_headers(method, path):
    server_time_json = requests.get("https://api.valr.com/v1/public/time").json()

    timestamp = server_time_json["epochTime"] * 1000
    secret = gen_signature(os.environ["VALR_API_SECRET"], timestamp, method, path)

    return {
        "X-VALR-API-KEY": os.environ["VALR_API_KEY"],
        "X-VALR-SIGNATURE": secret,
        "X-VALR-TIMESTAMP": str(timestamp),
    }


def market_summary():
    response = requests.get("https://api.valr.com/v1/public/BTCZAR/marketsummary")
    return response.json()


def balances():
    headers = gen_headers("GET", "/v1/account/balances")
    response = requests.get("https://api.valr.com/v1/account/balances", headers=headers)
    return response.json()


if __name__ == "__main__":
    print("MARKET SUMMARY")
    print(market_summary())
    print("BALANCES")
    print(balances())
