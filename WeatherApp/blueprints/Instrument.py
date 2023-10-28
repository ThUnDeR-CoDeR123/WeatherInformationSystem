from db.database import db
from datetime import datetime
class Instrument(db.Model):
    instrumentID = db.Column(db.Integer,nullable=False,unique=True)
    efficiency = db.Column(db.String(5),nullable=False,unique=True)
    Precision = db.Column(db.String(5),nullable=False)
    Installdate = db.Column(db.Date, default=datetime.now())
    LastRepair = db.Column(db.Date, default=datetime.now())