import socket
import json
import Constants
from communication import Connector
from logs import Logger
from _thread import *
from abc import abstractmethod


class Node:

    def __init__(self, pid, port, num_connections):
        self.pid = pid
        self.data = {}
        self.layer_nodes = {}
        self.backup_nodes = {}
        self.client_nodes = {}
        self.num_updates = 0
        web_connector = Connector.Connector()
        web_connector.connect('localhost', Constants.WEB_PORT)
        self.logger = Logger.Logger(pid, web_connector)
        start_new_thread(self.start_server, (port, num_connections,))

    def connect_to(self, pid, port, backup=False):
        connector = Connector.Connector()
        connector.connect('localhost', port)
        print(f"Connected to {pid}")
        connector.send_message(self.pid)
        if not backup:
            self.layer_nodes[pid] = connector
        else:
            self.backup_nodes[pid] = connector

    def start_server(self, port, num_connections):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', port))
        server_socket.listen()

        for i in range(num_connections):
            connector = Connector.Connector(server_socket)
            connector.accept_connection()
            pid = connector.receive_message()
            print(f"{pid} connected")
            self.client_nodes[pid] = connector
            start_new_thread(self.handle_connection, (connector,))

    @abstractmethod
    def handle_connection(self, connector):
        pass

    def read(self, msg):
        response = f"Index {msg['val']} of node {self.pid} is {self.data[msg['val']]}"
        self.client_nodes[msg['src']].send_message(response)

    def backup_broadcast(self, msg):
        for _, connector in self.backup_nodes.items():
            connector.send_message(msg)

    def new_update(self):
        self.num_updates += 1
        if not self.num_updates < Constants.LAZY_UPDATE_COUNT:
            msg = {'src': self.pid, 'op': "UPDATE", 'val': self.data}
            self.backup_broadcast(json.dumps(msg))
            self.num_updates = 0
