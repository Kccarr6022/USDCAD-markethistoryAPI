from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import datetime
import os

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) #base directory
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# USDCAD DATA
class POST(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.String(100), unique=True)
    close = db.Column(db.Float)
    

    def __init__(self, id, time, close):
        self.id = id
        self.time = time
        self.close = close

# Schema
class POSTSchema(ma.Schema):
    class Meta:
        fields = ('id', 'time', 'close')

# Init schema
product_schema = POSTSchema(strict =True)

# init data stream from trading view
usdcad = TA_Handler( 
    symbol="USDCAD", 
    screener="forex",
    exchange="FX_IDC", 
    interval=Interval.INTERVAL_4_HOURS,
    # proxies={'http': 'http://example.com:8080'} # Uncomment to enable proxy (replace the URL).
)
print(usdcad. get_analysis().indicators["close"])


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})

#run server
if __name__ == '__main__':
    app.run(debug=True)