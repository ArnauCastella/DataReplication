from nodes.Node import Node
import json
import queue
import time


class NodeA(Node):

    def __init__(self, pid, port):
        super().__init__(pid, port, 3)
        self.num_ack = 0
        self.queue = queue.Queue()

    def handle_msg(self, msg):
        if msg['op'] == "READ":
            self.read(msg)
        elif msg['op'] == "WRITE":
            self.num_ack = 0
            self.replicate(msg['val'])
            while self.num_ack < len(self.layer_nodes):
                pass
            self.update(msg['val'])
            self.new_update()
            self.layer_broadcast("ACK")
            self.client_nodes["CLIENT"].send_message("ACK")
        elif msg['op'] == "REPLICATE":
            self.num_ack = 0
            self.update(msg['val'])
            self.layer_nodes[msg['src']].send_message("ACK")
            self.new_update()
            while self.num_ack == 0:
                pass

    def handle_connection(self, connector):
        while True:
            msg = connector.receive_message()
            if msg == "CLIENT" or msg == "":
                continue
            if msg == "ACK":
                self.num_ack += 1
            else:
                try:
                    parsed_msg = json.loads(str(msg))
                    self.queue.put(parsed_msg)
                except json.JSONDecodeError as e:
                    print(e)

    def layer_broadcast(self, msg):
        for _, connector in self.layer_nodes.items():
            connector.send_message(msg)

    def replicate(self, val):
        msg = {'src': self.pid, 'op': "REPLICATE", 'val': val}
        self.layer_broadcast(json.dumps(msg))

    def update(self, val):
        pos = val.split(',')[0]
        value = val.split(',')[1]
        self.data[pos] = int(value)
        self.logger.write(str(self.data))

    def execute(self):
        while True:
            if not self.queue.empty():
                msg = self.queue.get()
                print("Handle: "+str(msg))
                self.handle_msg(msg)
