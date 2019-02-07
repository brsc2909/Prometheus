from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_socketio import SocketIO, emit
from prometheus.__main__ import tickers
import threading

app = Flask(__name__)
socketio = SocketIO(app)

NAMESPACE = '/test'


def test_message(message):
    """Example of how to send server generated events to clients."""
    resp = {"data": message}

    socketio.emit('push_book', resp, namespace=NAMESPACE)


@app.route("/")
def index():
    return render_template('index.html', tickers=tickers)


@socketio.on('connect', namespace=NAMESPACE)
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace=NAMESPACE)
def test_disconnect():
    print('Client disconnected')


class WebApp(object):

    def __init__(self, port):
        self.port = port
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()

    def run(self):
        socketio.run(app, port=self.port)
