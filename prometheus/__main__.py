#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prometheus import *
from exchanges.binance import Binance
from exchanges.GDAX import Gdax
from arbs import arbs
from decimal import Decimal
from webapp import server
import threading
import time

FEES = {'MAKER': Decimal(0.0001), 'TAKER': Decimal(0.0001)}

tickers = {
    'USDTUSDT': (1, 1),
    'BTCBTC': (1, 1),
    'ETCETC': (1, 1),
    'BNBBNB': (1, 1)
}


def main():
    global tickers

    binance = Binance(BINANCE_KEY, BINANCE_SECRET).client
    gdax = Gdax(GDAX_KEY, GDAX_SECRET, GDAX_PASSPHRASE).client

    btickers = binance.get_orderbook_tickers()
    for ticker in btickers:
        tickers[ticker['symbol']] = (Decimal(ticker['bidPrice']), Decimal(ticker['askPrice']))

    # start webapp thread
    server.WebApp(PORT)
    
    start = 1000
    symbols = ['TRX', 'BNB', 'ETH', 'BTC']

    count = 0
    while 1:
        count += 1
        server.test_message(btickers)
        time.sleep(1)
        # print("here")
        # arb = arbs.Arbs(tickers, FEES)
        # print(arb.multiarb(
        #     spend=start,
        #     base='USDT',
        #     symbols=symbols,
        #     profit=(start-1)
        # ))


if __name__ == '__main__':
    main()
