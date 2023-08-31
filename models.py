from sqlalchemy import Column, Date, Index, String, TIMESTAMP, Table, text, Integer
from sqlalchemy.schema import Sequence
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, Sequence("test_id_seq"), primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    gender = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255))
