from nodes import NodeA
import Constants
import time

if __name__ == '__main__':
    node = NodeA.NodeA("A2", Constants.PORT_A2)
    node.connect_to("A1", Constants.PORT_A1)
    node.connect_to("A3", Constants.PORT_A3)
    node.connect_to("B1", Constants.PORT_B1, True)

    node.execute()
