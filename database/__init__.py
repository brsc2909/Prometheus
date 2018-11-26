import sqlite3
from decimal import Decimal

DATABASE = '$HOME/PycharmProjects/Prometheus/prometheus.db'


def initdb():

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE test_order_book
                 (symbol, BID, ASK)
                 ''')
    c.close()
    conn.commit()
    conn.close()


def connect():
    return sqlite3.connect(DATABASE)


def put_tickers(tickers):
    tickers_array = []
    for symbol, (bid, ask) in tickers.items():
        tickers_array.append((symbol, str(bid), str(ask)))

    conn = connect()
    cur = conn.cursor()
    print(tickers_array)
    cur.executemany('INSERT INTO test_order_book VALUES (?, ?, ?)', tickers_array)
    conn.commit()
    print("tickers inserted")
    conn.close()


def get_order_book():
    order_book = {}
    conn = connect()
    cur = conn.cursor()

    for symbol, bid, ask in cur.execute('SELECT symbol, BID, ASK from test_order_book'):
        order_book[symbol] = (Decimal(bid), Decimal(ask))

    conn.close()

    return order_book
