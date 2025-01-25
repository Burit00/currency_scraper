from datetime import datetime
import env
from sqlalchemy import create_engine, select, text, Result, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, Session

from currency_model import Base, Currency, CurrencyValue

db_engine = create_engine(env.DATABASE__CONNECTION_STRING)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db_engine))

Base.query = db_session.query_property()

def add_currencies(currencies: [Currency]):
    with Session(db_engine) as session:
        session.add_all(currencies)
        session.commit()

def get_currencies() -> [Currency]:
    with Session(db_engine) as session:
        stmt = select(Currency)
        result = session.scalars(stmt)
        return list(result)

def add_currency_values(currencies: [CurrencyValue]):
    with Session(db_engine) as session:
        session.add_all(currencies)
        session.commit()

def get_currency_value_last_date() -> datetime:
    with Session(db_engine) as session:
        result = session.execute(text(f"SELECT MAX(date) FROM {CurrencyValue.__tablename__}"))
        return result.one()[0]

def get_currency_value_first_date() -> datetime:
    with Session(db_engine) as session:
        result = session.execute(text(f"SELECT MIN(date) FROM {CurrencyValue.__tablename__}"))
        return result.one()[0]

def get_currency_values(date_start: datetime = None, date_end: datetime = None, currencies: list[str] = env.CURRENCIES_LIST):
    with Session(db_engine) as session:
        stmt = select(CurrencyValue).where(CurrencyValue.currency_code.in_(currencies))

        if date_start is not None:
            stmt = stmt.where(date_start <= CurrencyValue.date)
        if date_end is not None:
            stmt = stmt.where(CurrencyValue.date <= date_end)

        result = session.scalars(stmt)
        return list(result)



def init_database():
    Base.metadata.create_all(bind=db_engine)


if __name__ == '__main__':
    init_database()

