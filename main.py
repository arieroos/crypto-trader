import sys
import time
from datetime import datetime

import error_handler
import valr
from extra_math import floor_n, subtract_nth_decimal

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

    # I had issues where VALR reported a higher btc balance than I actually had.
    # I suspect they haven't subtracted my fees yet. So let's give them some time.
    time.sleep(0.25)
    btc_bal = floor_n(valr.balance("BTC"))
    log(f"Bought BTC{btc_bal} at R{price}")

    new_price = int(price * (1 + (float(PERCENTAGE_TRADE) / 100.0)))
    btc_bal = subtract_nth_decimal(btc_bal, 8)
    # I had two occurrences where the balance I got back from VALR was exactly one sat too high.
    # I'd rather have a trade go through with one sat less than it can, than not have it go through at all.
    log(f"Placing a sell order for BTC{btc_bal} at R{new_price}")
    order = valr.limit_order(False, new_price, floor_n(btc_bal, 7))
    if not valr.order_placed(order):
        log(f"Order {order} failed")
    else:
        log(f"Order {order} successful")
