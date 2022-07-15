from datetime import datetime
from config import db, ma


class Person(db.Model):
    __tablename__ = 'person'

    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(40))
    fname = db.Column(db.String(40))
    timestamp = db.Column( db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PersonSchema(ma.Schema):
    class Meta:
        model = Person
        sqla_session = db.session


