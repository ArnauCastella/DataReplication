from nodes import NodeC
import Constants

if __name__ == '__main__':
    node = NodeC.NodeC("C1", Constants.PORT_C1)

    node.execute()