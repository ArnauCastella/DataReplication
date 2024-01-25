from nodes import NodeA
import Constants

if __name__ == '__main__':
    node = NodeA.NodeA("A3", Constants.PORT_A3)
    node.connect_to("A1", Constants.PORT_A1)
    node.connect_to("A2", Constants.PORT_A2)
    node.connect_to("B2", Constants.PORT_B2, True)

    node.execute()
