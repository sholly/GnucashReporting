import configparser

import piecash
from piecash import Account
from expensereport import PieCashConnectionManager


class DebtReport:

    def __init__(self, connMgr):
        self.connMgr = connMgr

    def debttesting(self):
        session = self.connMgr.getSession()

        liabilityAccounts = session.query(Account).filter(
            Account.type == "LIABILITY").all()

        for l in liabilityAccounts:
            print(l.name)

        book = self.connMgr.getBook()
        creditAccounts = session.query(Account).filter(
            Account.type == "CREDIT").all()

        for c in creditAccounts:
            print(c.name)
            print(c.sum())

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('./gnucashreporting.ini')
    connMgr = PieCashConnectionManager(config['development']['username'],
                                       config['development']['password'],
                                       config['development']['host'])

    dr = DebtReport(connMgr)
    dr.debttesting()

