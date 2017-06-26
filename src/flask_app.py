import configparser
import datetime
import decimal

import flask.json
from flask import Flask, jsonify, request
from flask_cors import CORS

from debtreport import DebtReport
from expensereport import ExpenseReport, Expense
from PieCashConnectionManager import PieCashConnectionManager


# api = Api(app)
def firstdayofmonth():
    today = datetime.date.today()
    first_day = today.replace(day=1)
    return datetime.datetime.combine(first_day, datetime.datetime.min.time())

class DecimalJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(DecimalJSONEncoder, self).default(obj)


class FlaskExpenseEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Expense):
            return obj.toJSON()
        return super(FlaskExpenseEncoder, self).default(obj)


app = Flask(__name__)
app.config.from_envvar('GNUCASHREPORTS_SETTINGS')
CORS(app)
app.json_encoder = FlaskExpenseEncoder


# def readconfig():
#     config = configparser.ConfigParser();
#     config.read('gnucashreporting.ini')
#     return config

@app.route('/expenses')
def get_expenses():
    # config = readconfig()
    connmgr = PieCashConnectionManager(app.config['DB_USERNAME'],
                                       app.config['DB_PASSWORD'],
                                       app.config['DB_HOST'])
    expensereport = ExpenseReport(connmgr)

    if (request.args.get('startdate') is not None):
        startdate = datetime.datetime.strptime(request.args.get('startdate'), "%Y-%m-%d")
    else:
        # startdate = datetime.datetime.strptime("2017-04-01", "%Y-%m-%d")
        startdate = firstdayofmonth()
    if (request.args.get('enddate') is not None):
        enddate = datetime.datetime.strptime(request.args.get('enddate'), "%Y-%m-%d")
    else:
        enddate = datetime.datetime.today()
    return jsonify(expensereport.getexpenses(startdate, enddate))

@app.route('/debt')
def debtreport():

    connmgr = PieCashConnectionManager(app.config['DB_USERNAME'],
                                       app.config['DB_PASSWORD'],
                                       app.config['DB_HOST'])
    debtreport = DebtReport(connmgr)
    startdate = datetime.datetime.strptime("2013-01-01", "%Y-%m-%d");
    enddate = datetime.datetime.today()

    accounts = ["CU of CO Visa", "Lending Club", "Paypal Mastercard", "AMZN Chase Visa", "CapOne Platinum"]
    # accounts = ["CU of CO Visa", "Lending Club", "Paypal Mastercard", "AMZN Chase Visa"]
    # accounts = [ "CU of CO Visa", "Paypal Mastercard"]
    return jsonify(debtreport.sumovertime(accounts, startdate, enddate))


# api.add_resource(Expenses, '/expensereport')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
