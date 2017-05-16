import configparser
import datetime
from sqlalchemy.orm import joinedload
from piecash import Account, Transaction, Split
from expensereport import PieCashConnectionManager


class DebtReport:

    def __init__(self, connMgr):
        self.connMgr = connMgr

    def accountsum(self, accountname, startdate):
        session = self.connMgr.getSession()

        debttransactions = session.query(Transaction, Split, Account).\
            filter(Transaction.guid == Split.transaction_guid,
                   Split.account_guid == Account.guid,
                   Account.name == accountname ,
                   Transaction.post_date <= startdate).all()


        sum = 0;

        for t in debttransactions:
            sum += t[1].value
        print(accountname, ",", sum)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('./gnucashreporting.ini')
    connMgr = PieCashConnectionManager(config['development']['username'],
                                       config['development']['password'],
                                       config['development']['host'])

    dr = DebtReport(connMgr)
    dr.accountsum("CU of CO Visa", datetime.datetime.today());
    dr.accountsum("Lending Club", datetime.datetime.today());
    dr.accountsum("Paypal", datetime.datetime.today());
    dr.accountsum("AES Student Loan", datetime.datetime.today());
    dr.accountsum("Nelnet Student Loan", datetime.datetime.today());
    dr.accountsum("CU of CO Visa", datetime.datetime.strptime("2017-08-01", "%Y-%m-%d"));

