#!/usr/bin/env python
###########################################################################################
# Author: Brendan Scullion (brsc2909)
# Email: brsc2909@Gmial.com
# Date: 07/01/2018
# Description:
#   module for interacting with the difference crypto currency exchanges
###########################################################################################
from binance.client import Client
from binance import enums as binance_enums
import requests
import time

ENUMS = binance_enums


class Binance(object):
    client = None

    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_accounts(self):
        return self.client.get_account()

    def depth(self, symbol_pair):
        return self.client.get_order_book(symbol=symbol_pair)

    def getalltickers(self):
        return self.client.get_all_tickers()

    def latency(self):
        up = time.time() * 1000
        server_time = self.client.get_server_time()['serverTime']
        down = time.time() * 1000
        return {
            "up": server_time - up,
            "down": down - server_time,
            "rt": down - up
        }

    def crypto_withdraw(self, qty, asset, address):
        # check docs for assumptions around withdrawals
        from binance.exceptions import BinanceAPIException, BinanceWithdrawException
        try:
            result = self.client.withdraw(
                asset=asset,
                address=address,
                amount=qty)
        except BinanceAPIException as e:
            print(e)
        except BinanceWithdrawException as e:
            print(e)
        else:
            print("Success")


def get_fees():
    r = requests.get(url='https://www.binance.com/assetWithdraw/getAllAsset.html')
    return r.json()


def get_exchange_info():
    return requests.get(url='https://api.binance.com/api/v1/exchangeInfo').json()
