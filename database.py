import sys
import oracledb
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import oracledb
# import lsnr_stat
import sys
import os

instantclient_dir = 'instantclient'
if getattr(sys, 'frozen', False):
    instaclient_dir = os.path.join(sys._MEIPASS, instantclient_dir)
    # Add Oracle Client library directory to PATH
    os.environ['PATH'] = instantclient_dir + os.path.pathsep + os.environ['PATH']

# service_name = lsnr_stat.get_service_name()
# MYSQL_DATABASE_URI = "sqlite:///database.db"
oracledb.init_oracle_client(lib_dir=instantclient_dir)

ORACLE_DATABASE_URI = f"oracle+oracledb://test:root@172.16.17.63:1521/xe"

engine = create_engine(
    ORACLE_DATABASE_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
