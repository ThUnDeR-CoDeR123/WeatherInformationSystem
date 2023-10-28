
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db.singleton import db


# ________________________________________________________________TABLE RELATION________________________________________________________________
complain_instrument = db.Table('complain_instrument',
                               db.Column("Engineer_id", db.Integer,db.ForeignKey('engineer.Id')),
                               db.Column("Complain_id", db.Integer,db.ForeignKey('complain.Id'))
                            
)   
#________________________________________________________________MODELS________________________________________________________________


class Admin(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return f'<Admin: {self.name}>'

class Engineer(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return f'<Engineer: {self.name}>'
    
class StManager(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return f'<StManager: {self.name}>'

class Complain(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    instrumentID = db.Column(db.Integer,db.ForeignKey('instrument.Id'))
    details = db.Column(db.String(80),nullable=False)
    date = db.Column(db.Date, default=datetime.now())
    Resolvedby = db.relationship('Engineer',secondary=complain_instrument,backref='Assignments')
    is_active = db.Column(db.Boolean, unique=False, default=True)
    

    def __repr__(self):
        return f'<Complain: {self.Id}>'
                               


class Instrument(db.Model):
    Id = db.Column(db.Integer,primary_key=True)
    efficiency = db.Column(db.String(5),nullable=False,unique=True)
    Precision = db.Column(db.String(5),nullable=False)
    Installdate = db.Column(db.Date, default=datetime.now())
    LastRepair = db.Column(db.Date, default=datetime.now())
    Complains = db.relationship("Complain",backref="instrument")
    def __repr__(self):
        return f'<Instrument: {self.Id}>'