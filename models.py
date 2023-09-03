from sqlalchemy import Column, Date, Index, String, TIMESTAMP, Table, text, Integer
from sqlalchemy.schema import Sequence
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SKU_EXL(Base):
    __tablename__ = "SKU_EXL"
    id = Column(Integer, Sequence("test_id_seq"), primary_key=True)
    SKU_Code = Column(String(255))
    LOT_No = Column(String(255))
    Serial_No = Column(String(255))
