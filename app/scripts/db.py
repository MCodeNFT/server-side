import os

from sqlalchemy import create_engine
from sqlalchemy import String, Integer, Column, Index
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = os.environ.get('database_url',  "postgresql://ligulfzhou:POSTGRESzlg153@localhost:5432/mcode")
base = declarative_base()


class MCode(base):
    __tablename__ = 'mcode'

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    name = Column(String)
    description = Column(String)
    word_list = Column(ARRAY(String))
    attributes = Column(ARRAY(JSON))


mcode_index = Index('mcode_index', MCode.index)


class Db:
    def __init__(self):
        db_engine = create_engine(db_string)
        self._create_tb_and_index(db_engine)
        session = sessionmaker(db_engine)
        self.session = session()

    def _create_tb_and_index(self, db_engine):
        base.metadata.create_all(db_engine)
        # index only need to create once...
        # log_index.create(bind=db_engine)

    def add_mcode(self, data: dict):
        self.add_model('MCode', data)

    def add_model(self, model: str, data: dict):
        m = eval(model)(**data)
        try:
            self.session.add(m)
            self.session.commit()
        except Exception as e:
            print(f'insert {model} with {data} fail with {e}')
            self.session.rollback()
