from db.database import db
class Admin(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    usernames = db.Column(db.String(80),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)