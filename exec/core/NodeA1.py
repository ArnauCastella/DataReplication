from nodes import NodeA
import Constants
import time

if __name__ == '__main__':
    node = NodeA.NodeA("A1", Constants.PORT_A1)
    node.connect_to("A2", Constants.PORT_A2)
    node.connect_to("A3", Constants.PORT_A3)

    node.execute()
