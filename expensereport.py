import datetime
import piecash
import configparser
import json
from json import JSONEncoder
import decimal
from piecash import Split, Transaction, Book
from sqlalchemy.orm import joinedload


# username = "gnucash"
# password = "PhuckIt"
# host = "127.0.0.1"
# book = piecash.open_book(uri_conn="mysql://" + username + ":" + password + "@" +
#                                   host + ":3306/gnucash")


class PieCashConnectionManager():
    def __init__(self, username, password, host, port='3306', database='gnucash'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.book = None
        self.session = None
        self._buildconnectionstring()

    def _buildconnectionstring(self):
        self.connString = "mysql://" + self.username + ":" + self.password + "@" + \
                          self.host + ":" + self.port + "/" + self.database

    def getBook(self):
        self.book = piecash.open_book(uri_conn=self.connString)
        return self.book

    def getSession(self):
        if self.book is None:
            self.getBook()
        self.session = self.book.session
        return self.session


class Expense():
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def addamount(self, amount):
        self.amount += amount

    def __repr__(self):
        return self.name + " " + str(self.amount)

    def toJSON(self):
        return {'name': self.name, 'amount': str(self.amount)}


class ExpenseEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Expense):
            return obj.toJSON();


class ExpenseReport():
    def __init__(self, connMgr):
        self.connMgr = connMgr

    def getexpenses(self, startdate, enddate=datetime.datetime.now()):
        session = None
        session = self.connMgr.getSession()
        expenses = {}

        print("start transactions query")
        transactions = session.query(Transaction). \
            options(joinedload('splits')).filter(
            Transaction.post_date >= startdate,
            Transaction.post_date <= enddate
        ).all()
        print("end transactions query")

        # transactions.sort(key=lambda x: x.enter_date)
        print("start summarizing expenses..")
        splitcount = 0
        for t in transactions:
            for split in t.splits:
                splitcount += 1
                if (split.account.type == "EXPENSE"):
                    # print(split.account.fullname)
                    # print(split.value)
                    accountname = split.account.name
                    if accountname in expenses:
                        # expenses[accountname] += split.value
                        expenses[accountname].addamount(split.value)
                    else:
                        # expenses[accountname] = split.value
                        expenses[accountname] = Expense(split.account.name, split.value)
        print("end summarizing expenses..")

        # sortedexpenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
        # expensesjson = json.dumps(sortedexpenses, default=self.defaultencodedecimal)
        # return expensesjson
        # print(type(sortedexpenses))
        # return sortedexpenses

        # for key, value in expenses.items():
        #     print(value)

        sortedexpenses = sorted(expenses.values(), key=lambda x: x.amount, reverse=True)
        return sortedexpenses;

    def defaultencodedecimal(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('gnucashreporting.ini')
    connMgr = PieCashConnectionManager(config['development']['username'],
                                       config['development']['password'],
                                       config['development']['host'])
    print(connMgr.connString)
    expensereport = ExpenseReport(connMgr)

    startdate = datetime.datetime.strptime("2012-04-01", "%Y-%m-%d")
    # enddate = datetime.datetime.strptime("2017-12-31", "%Y-%m-%d")
    enddate = datetime.datetime.today()
    expenses = expensereport.getexpenses(startdate, enddate)

    print(json.dumps(expenses, cls=ExpenseEncoder, indent=4))
