from nodes import NodeB
import Constants

if __name__ == '__main__':
    node = NodeB.NodeB("B2", Constants.PORT_B2)
    node.connect_to("C1", Constants.PORT_C1, True)
    node.connect_to("C2", Constants.PORT_C2, True)

    node.execute()
