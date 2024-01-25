from transactions import TransactionManager
import Constants

if __name__ == '__main__':
    transactions_mgr = TransactionManager.TransactionManager()
    transactions_mgr.connect_nodes()

    file = open("../"+Constants.TRANSACTIONS_PATH, "r")
    for line in file:
        transactions = TransactionManager.get_transactions(line)
        transactions_mgr.send_transactions(transactions)
