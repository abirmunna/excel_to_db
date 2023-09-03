import sys
import oracledb
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import lsnr_stat

service_name = lsnr_stat.get_service_name()
# MYSQL_DATABASE_URI = "sqlite:///database.db"
ORACLE_DATABASE_URI = f"oracle+oracledb://test:root@localhost:1521/{service_name}"

engine = create_engine(
    ORACLE_DATABASE_URI, thick_mode={"lib_dir": r"instantclient"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
