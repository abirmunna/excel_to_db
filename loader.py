import pandas as pd
from database import SessionLocal, engine
from models import Test, Base
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
rprint(df.head())

def pandas_df_to_db(df: pd.DataFrame, db: Session) -> None:
    for index, data in df.iterrows():
        data = Test(first_name=data.FirstName,
                    last_name=data.LastName,
                    gender=data.Gender,
                    phone=data.Phone,
                    email=data.Email)
        rprint(data)
        db.add(data)
        db.commit()
        db.refresh(data)

pandas_df_to_db(df, db)
