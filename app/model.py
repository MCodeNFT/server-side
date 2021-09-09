from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MLoot(db.Model):
    __tablename__ = 'mloot'

    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    name = db.Column(db.String)
    description = db.Column(db.String)
    word_list = db.Column(db.ARRAY(db.String))
    attributes = db.Column(db.ARRAY(db.JSON))
