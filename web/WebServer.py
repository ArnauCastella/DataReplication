from flask import Flask, render_template
from flask_socketio import SocketIO

import Constants
from communication import Connector
import socket
from _thread import *
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'holi'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


def send_data(node, data):
    send = {'node': node, 'data': data}
    socketio.emit('update_message', send)


def handle_connection(c):
    while True:
        msg = json.loads(c.receive_message())
        send_data(msg['src'], msg['data'])


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', Constants.WEB_PORT))
    server_socket.listen()

    for i in range(Constants.NUM_NODES):
        connector = Connector.Connector(server_socket)
        connector.accept_connection()
        print("New connection")
        start_new_thread(handle_connection, (connector,))

    socketio.run(app, port=12000, allow_unsafe_werkzeug=True)
