from communication import Connector
import Constants
import random
import json
import time


def wait_ack(connector):
    if connector.receive_message() == "ACK":
        pass
    else:
        print("Expected ACK")
        exit(-1)


def get_transactions(line):
    attrs = line.split(", ")

    if attrs[0] != "b":
        dest = attrs[0][1:]
    else:
        dest = 0

    transactions = []
    for attr in attrs[1:-1]:
        transaction = {'dest': dest, 'val': attr[2:-1]}
        if attr[0] == "r":
            transaction['op'] = "READ"
        else:
            transaction['op'] = "WRITE"

        transactions.append(transaction)

    return transactions


class TransactionManager:

    def __init__(self):
        self.nodes = {}

    def connect_nodes(self):
        self._connect_node(Constants.PORT_A1, "A1")
        self._connect_node(Constants.PORT_A2, "A2")
        self._connect_node(Constants.PORT_A3, "A3")
        self._connect_node(Constants.PORT_B1, "B1")
        self._connect_node(Constants.PORT_B2, "B2")
        self._connect_node(Constants.PORT_C1, "C1")
        self._connect_node(Constants.PORT_C2, "C2")

    def _connect_node(self, port, pid):
        connector = Connector.Connector()
        connector.connect('localhost', port)
        connector.send_message("CLIENT")
        self.nodes[pid] = connector

    def send_transactions(self, transactions):
        for transaction in transactions:
            msg = {'src': "CLIENT", 'op': transaction['op'], 'val': transaction['val']}

            if msg['op'] == "WRITE":
                i = random.randint(1, 3)
                dest_id = "A" + str(i)
                self.nodes[dest_id].send_message(json.dumps(msg))
                print(dest_id+" "+str(msg))
                wait_ack(self.nodes[dest_id])
            else:
                i = random.randint(1, 2)
                if transaction['dest'] == "1":
                    dest_id = "B" + str(i)
                elif transaction['dest'] == "2":
                    dest_id = "C" + str(i)
                else:
                    i = random.randint(1, 3)
                    dest_id = "A" + str(i)
                self.nodes[dest_id].send_message(json.dumps(msg))
                print(dest_id+" "+str(msg))
                print(self.nodes[dest_id].receive_message())

            # time.sleep(1)
