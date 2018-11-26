import configparser
import gdax


class Gdax(object):

    client = None
    config = configparser.ConfigParser()
    config.read("prometheus.cnf")
    api_key = config.get('GDAX', 'api_key')
    api_secret = config.get('GDAX', 'api_secret')
    api_passphrase = config.get('GDAX', 'api_passphrase')

    def __init__(self):
        self.client = gdax.AuthenticatedClient(
        self.api_key,
        self.api_secret,
        self.api_passphrase)

    def getAccounts(self):
        return self.client.get_accounts()

    def getAccount(self, account):
        return self.client.get_account(account)

    def crypto_withdraw(self, qty, asset, crypto_address):
        payload = {
            "amount": qty,
            "currency": asset,
            "crypto_address": crypto_address
        }
        return self.client.crypto_withdraw()
