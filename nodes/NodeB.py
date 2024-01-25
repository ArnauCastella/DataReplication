from nodes.Node import Node
import json
import queue
import time


class NodeB(Node):

    def __init__(self, pid, port):
        super().__init__(pid, port, 2)
        self.queue = queue.Queue()

    def handle_msg(self, msg):
        if msg['op'] == "READ":
            self.read(msg)
        elif msg['op'] == "UPDATE":
            self.update(msg['val'])

    def handle_connection(self, connector):
        while True:
            msg = connector.receive_message()

            if msg == "CLIENT" or msg == "":
                continue
            else:
                try:
                    parsed_msg = json.loads(str(msg))
                    self.queue.put(parsed_msg)
                except json.JSONDecodeError as e:
                    print(e)

    def update(self, val):
        self.data = val
        self.logger.write(str(self.data))

    def execute(self):
        start = time.time()
        while True:
            if time.time() - start >= 1:
                self.new_update()
                start = time.time()
            if not self.queue.empty():
                msg = self.queue.get()
                print("Handle: "+str(msg))
                self.handle_msg(msg)
