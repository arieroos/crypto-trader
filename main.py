import sys
from datetime import datetime

import error_handler
import valr
from extra_math import floor_n

MIN_ZAR = 50
PERCENTAGE_TRADE = 0.5


def log(msg: str):
    print(f"[{datetime.now()}] {msg}", flush=True)


if __name__ == "__main__":
    sys.excepthook = error_handler.excepthook

    zar_bal = floor_n(valr.balance("ZAR"), 2)
    if zar_bal < MIN_ZAR:
        log(f"Current balance of R{zar_bal} is too small, less than {MIN_ZAR}, doing nothing")
        exit()

    buy_amt = floor_n(zar_bal / 4, 2)
    if buy_amt < MIN_ZAR:
        buy_amt = float(MIN_ZAR)
    log(f"Buying R{buy_amt} worth of BTC at market")
    price = valr.buy_at_market(buy_amt)
    btc_bal = valr.balance("BTC")
    log(f"Bought BTC{btc_bal} at R{price}")

    new_price = int(price * (1 + (float(PERCENTAGE_TRADE) / 100.0)))
    log(f"Placing a sell order at R{new_price}")
    order = valr.limit_order(False, new_price, btc_bal)
    if not valr.order_placed(order):
        log(f"Order {order} failed")
    else:
        log(f"Order {order} successful")
