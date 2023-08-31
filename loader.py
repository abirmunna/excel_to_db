import pandas as pd
from database import SessionLocal, engine
from models import Test, Base
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Union, Optional
from rich import print as rprint

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db: Session = next(get_db())


def load_data_from_excel(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath)
    return df


df = load_data_from_excel("data/test.xlsx")


def pandas_df_to_db(df: pd.DataFrame, db: Session) -> None:
    for index, data in df.iterrows():
        # if not db.query(Test).filter(Test.email == data.Email).first():
        data = Test(
            first_name=data.FirstName,
            last_name=data.LastName,
            gender=data.Gender,
            phone=data.Phone,
            email=data.Email,
        )
        db.add(data)
        db.commit()


# pandas_df_to_db(df, db)


def drop_table(db: Session, table: Union[str, Test]) -> None:
    if isinstance(table, str):
        db.execute(text(f"DROP TABLE {table}"))
    else:
        db.execute(text(f"DROP TABLE {table.__tablename__}"))
    db.commit()


drop_table(db, Test)
