import sys
import oracledb
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

# MYSQL_DATABASE_URI = "sqlite:///database.db"
ORACLE_DATABASE_URI = "oracle+oracledb://test:root@localhost:1521/xe"

engine = create_engine(
    ORACLE_DATABASE_URI, thick_mode={"lib_dir": r"E:\downloads\instantclient"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
