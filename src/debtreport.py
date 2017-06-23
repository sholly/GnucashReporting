import configparser
import datetime
from dateutil import relativedelta
import pytz
from sqlalchemy.orm import joinedload
from piecash import Account, Transaction, Split
from PieCashConnectionManager import PieCashConnectionManager


def first_day_of_month(date):
    first_day = date.replace(day=1)
    return first_day

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

class DebtReport:
    def __init__(self, connMgr):
        self.connMgr = connMgr

    def debtaccounts(self, enddate):
        session = self.connMgr.getSession()

        debttransactions = session.query(Transaction, Split, Account). \
            filter(Transaction.guid == Split.transaction_guid,
                   Split.account_guid == Account.guid,
                   Account.type == "LIABILITY",
                   Transaction.post_date <= startdate).all()

        for d in debttransactions:
            print(d[2].fullname)
            print(d[1].value)

    def accountsum(self, accountname, startdate):
        session = self.connMgr.getSession()

        debttransactions = session.query(Transaction, Split, Account). \
            filter(Transaction.guid == Split.transaction_guid,
                   Split.account_guid == Account.guid,
                   Account.name == accountname,
                   Transaction.post_date <= startdate).all()
        sum = 0;

        for t in debttransactions:
            sum += t[1].value
        print(accountname, ",", sum)

    def sumforaccount(self, accountname, startdate, enddate):
        session = self.connMgr.getSession()

        things = session.query(Transaction, Split, Account). \
            filter(Transaction.guid == Split.transaction_guid,
                   Split.account_guid == Account.guid,
                   Account.name == accountname,
                   Transaction.post_date <= enddate).all()

        monthdate = startdate
        enddatetz = enddate.replace(tzinfo=pytz.UTC)
        monthdate = monthdate.replace(tzinfo=pytz.UTC)
        databymonth = {}
        while(monthdate < enddatetz):
            sum = 0
            for t in things:
                postdate = t[0].post_date
                if postdate <= monthdate:
                    sum += t[1].value
            databymonth[str(monthdate)] = str(sum)
            monthdate += relativedelta.relativedelta(months=1)

        sum = 0
        for t in things:
            postdate = t[0].post_date
            if postdate <= enddatetz:
                sum += t[1].value
            databymonth[str(enddate)] = str(sum)

        return databymonth

    def sumovertime(self, accountlist, startdate, enddate):
        accountsdata = {}
        for account in accountlist:
            accountdata = self.sumforaccount(account, startdate, enddate)
            accountsdata[account] = accountdata

        return accountsdata




if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('./gnucashreporting.ini')
    connMgr = PieCashConnectionManager(config['development']['username'],
                                       config['development']['password'],
                                       config['development']['host'])

    dr = DebtReport(connMgr)
    # dr.accountsum("CU of CO Visa", datetime.datetime.today());
    # dr.accountsum("Lending Club", datetime.datetime.today());
    # dr.accountsum("Paypal", datetime.datetime.today());
    # dr.accountsum("AES Student Loan", datetime.datetime.today());
    # dr.accountsum("Nelnet Student Loan", datetime.datetime.today());
    # dr.accountsum("CU of CO Visa", datetime.datetime.strptime("2017-09-01", "%Y-%m-%d"));
    #dr.accountsum("CU of CO Visa", datetime.datetime.today());
    startdate = datetime.datetime.strptime("2014-02-01", "%Y-%m-%d");
    enddate = datetime.datetime.today()
    #data = dr.sumforaccount("CU of CO Visa", startdate, enddate)
    accounts = ["Paypal", "Lending Club", "CU of CO Visa", "AES Student Loan", "CapOne Platinum"]
    accountsdata = dr.sumovertime(accounts, startdate, enddate)

    for k, v in accountsdata.items():
        print(k)
        for k1, v1 in v.items():
            print(k1, v1)

