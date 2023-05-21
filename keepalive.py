from flask import Flask
from threading import Thread

app = Flask('app')


@app.route('/')
def maun():
    return 'Test bot working'


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()
