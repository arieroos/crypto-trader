import sys
from datetime import datetime

import error_handler
import valr

UNKNOWN_TREND = "unknown"
DOWN_TREND = "down"
UP_TREND = "up"


def log(msg: str):
    print(f"[{datetime.now()}] {msg}", flush=True)


if __name__ == "__main__":
    sys.excepthook = error_handler.excepthook

    orders = [x for x in valr.get_open_orders() if x["side"].upper() == "BUY"]
    if len(orders) > 0:
        log("open orders found: closing")
        valr.close_open_buys()

        market_summary = valr.market_summary()
        base_price = float(market_summary["lastTradedPrice"])
    else:
        sell_price = valr.sell_at_market()
        log(f"Sold at {sell_price}")
        base_price = sell_price

    percentage = 0.33 / 100.0
    buy_adjustment = 1 - percentage
    buy_price = base_price * buy_adjustment
    log(f"Placing buy order at {buy_price}")
    valr.buy_order(buy_price)
    log("Buy order placed")
