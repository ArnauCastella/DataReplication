from nodes import NodeB
import Constants

if __name__ == '__main__':
    node = NodeB.NodeB("B1", Constants.PORT_B1)

    node.execute()
