from sqlalchemy import Column, Date, Index, String, TIMESTAMP, Table, text, Integer
from sqlalchemy.schema import Sequence
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Test(Base):
    __tablename__ = 'test'
    id_seq = Sequence("id_seq")
    id = Column(Integer, id_seq, primary_key=True, server_default=id_seq.next_value())
    first_name = Column(String(255))
    last_name = Column(String(255))
    gender = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255))
