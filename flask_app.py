from flask import Flask, jsonify, request
import flask.json
from flask_cors import CORS
import configparser
import datetime
import decimal
from expensereport import ExpenseReport, PieCashConnectionManager

# api = Api(app)

class DecimalJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(DecimalJSONEncoder, self).default(obj)

app = Flask(__name__)
CORS(app)
app.json_encoder = DecimalJSONEncoder
def readconfig():
    config = configparser.ConfigParser();
    config.read('gnucashreporting.ini')
    return config

@app.route('/expenses')
def get_expenses():
    config = readconfig()
    connmgr = PieCashConnectionManager(config['development']['username'],
                                       config['development']['password'],
                                       config['development']['host'])
    expensereport = ExpenseReport(connmgr)

    if(request.args.get('startdate')is not None):
        startdate = datetime.datetime.strptime(request.args.get('startdate'), "%Y-%m-%d")
    else:
        startdate = datetime.datetime.strptime("2012-01-01", "%Y-%m-%d")

    if(request.args.get('enddate') is not None):
        enddate = datetime.datetime.strptime(request.args.get('enddate'), "%Y-%m-%d")
    else:
        enddate = datetime.datetime.today()
    return jsonify(items=expensereport.getexpenses(startdate, enddate))
#class Expenses(Resource):
#    def get(self):
#        config = readconfig()
#        connmgr = PieCashConnectionManager(config['development']['username'],
#                                           config['development']['password'],
#                                           config['development']['host'])
#        expensereport = ExpenseReport(connmgr)
#
#        startdate = datetime.datetime.strptime("2017-04-01", "%Y-%m-%d")
#        #enddate = datetime.datetime.strptime("2017-, "%Y-%m-%d")
#        return {"expenses" : expensereport.getexpenses(startdate)}
#api.add_resource(Expenses, '/expensereport')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)