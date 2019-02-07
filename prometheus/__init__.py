import argparse
import configparser


def args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Path to config file", type=str,
                        default='/home/bscullion/PycharmProjects/Prometheus/prometheus.cnf')
    parser.parse_args()

    return parser.parse_args()


def configs():

    config = configparser.ConfigParser()
    config.read(args().config)

    return config


BINANCE_KEY = configs().get('BINANCE', 'api_key')
BINANCE_SECRET = configs().get('BINANCE', 'api_secret')
PORT = configs().get('WEBAPP', 'port')

GDAX_KEY = configs().get('GDAX', 'api_key')
GDAX_SECRET = configs().get('GDAX', 'api_secret')
GDAX_PASSPHRASE = configs().get('GDAX', 'api_passphrase')
