from flask import g
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import TIMESTAMP

db = SQLAlchemy()


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    raw_log = db.Column(db.ARRAY(db.String))
    processed_log = db.Column(db.ARRAY(db.String))
    error_line = db.Column(db.String)
    error_line_regex = db.Column(db.String)
    self_generate_regex = db.Column(db.String)
    loop_output_regex = db.Column(db.ARRAY(db.String))
    is_temp = db.Column(db.Boolean, default=False)
    create_time = db.Column(TIMESTAMP, default=datetime.datetime.now)

    def __repr__(self):
        return f'<Log {self.url}'
