#!/usr/bin/env python
from prometheus import *
from exchanges.binance import Binance
from arbs import arbs
from decimal import Decimal

FEES = {'MAKER': Decimal(0.0000150), 'TAKER': Decimal(0.00030)}


def main():
    binance_client = Binance(BINANCE_KEY, BINANCE_SECRET).client

    tickers = {
        'USDTUSDT': (1, 1),
        'BTCBTC': (1, 1),
        'ETCETC': (1, 1),
        'BNBBNB': (1, 1)
    }

    for ticker in binance_client.get_orderbook_tickers():
        tickers[ticker['symbol']] = (Decimal(ticker['bidPrice']), Decimal(ticker['askPrice']))

    start = 1000
    symbols = ['TRX', 'BNB', 'ETH', 'BTC']

    while 1:
        print("here")
        arb = arbs.Arbs(tickers, FEES)
        print(arb.multiarb(
            spend=start,
            base='USDT',
            symbols=symbols,
            profit=(start-1)
        ))


if __name__ == '__main__':
    main()
