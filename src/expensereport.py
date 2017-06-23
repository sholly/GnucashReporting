import configparser
import datetime
import decimal
from json import JSONEncoder

from piecash import Transaction
from sqlalchemy.orm import joinedload

from PieCashConnectionManager import PieCashConnectionManager


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
        expenses = {}

        transactions = self._gettransactions(startdate, enddate)

        for t in transactions:
            for split in t.splits:
                if split.account.type == "EXPENSE":
                    accountname = split.account.name
                    if accountname in expenses:
                        expenses[accountname].addamount(split.value)
                    else:
                        expenses[accountname] = Expense(accountname, split.value)

        sortedexpenses = sorted(expenses.values(), key=lambda x: x.amount, reverse=True)
        return sortedexpenses;

    def _gettransactions(self, startdate, enddate):
        session = self.connMgr.getSession()
        transactions = session.query(Transaction). \
            options(joinedload('splits')).filter(
            Transaction.post_date >= startdate,
            Transaction.post_date <= enddate
        ).all()
        return transactions

    def defaultencodedecimal(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)

def first_day_of_month(date):
    first_day = date.replace(day=1)
    return first_day

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('./gnucashreporting.ini')
    connMgr = PieCashConnectionManager(config['development']['username'],
                                       config['development']['password'],
                                       config['development']['host'])
    print(connMgr.connString)
    expensereport = ExpenseReport(connMgr)

    startdate = datetime.datetime.strptime("2015-04-01", "%Y-%m-%d")
    enddate = datetime.datetime.today()
    expenses = expensereport.getexpenses(startdate, enddate)

    # print(json.dumps(expenses, cls=ExpenseEncoder, indent=4))
    # for expense in expenses:
    #     print(expense)
    print(type(expenses))
