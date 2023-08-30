from sqlalchemy import Column, Date, Index, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Test(Base):
    __tablename__ = 'test'
    id = Column(INTEGER(11), primary_key=True)
    first_name = Column(VARCHAR(255))
    last_name = Column(VARCHAR(255))
    gender = Column(VARCHAR(255))
    phone = Column(VARCHAR(255))
    email = Column(VARCHAR(255))
