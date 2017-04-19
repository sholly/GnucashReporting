import datetime
import piecash
from piecash import Split, Transaction, Book

username = "test"
password = "pleaseignore"
host = "10.10.0.2"
book = piecash.open_book(uri_conn="mysql://" + username + ":" + password + "@" +
                                  host + ":3306/gnucash")


def expensereport():
    session = book.session
    expenses = {}

    today = datetime.datetime.now()
    startofmonthdate = datetime.datetime(2012, 1, 1)
    transactions = session.query(Transaction).filter(
        Transaction.post_date <= today,
        Transaction.post_date >= startofmonthdate
    ).all()

    # transactions.sort(key=lambda x: x.enter_date)
    splitcount = 0
    for t in transactions:
        for split in t.splits:
            splitcount += 1
            if(split.account.type == "EXPENSE"):
                # print(split.account.fullname)
                # print(split.value)
                accountname = split.account.fullname
                if accountname in expenses:
                    expenses[accountname] += split.value
                else:
                    expenses[accountname] = split.value

    sortedexpenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    for e in sortedexpenses:
        print(e)
    print("split count ", splitcount)

if __name__ == "__main__":
    expensereport()
