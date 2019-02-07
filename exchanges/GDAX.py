import cbpro as gdax


class Gdax(object):

    def __init__(self, api_key, api_secret, api_passphrase):
        self.client = gdax.AuthenticatedClient(
            api_key,
            api_secret,
            api_passphrase)
