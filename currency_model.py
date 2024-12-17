from datetime import datetime
from typing import List, Any

from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import Mapped, relationship, declarative_base
from sqlalchemy.testing.schema import mapped_column


Base = declarative_base()

class Currency(Base):
    __tablename__ = 'currencies'

    code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    symbol: Mapped[str]
    values: Mapped[List["CurrencyValue"]] = relationship(back_populates="currency", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Currency(code={self.code}; name={self.name}; symbol={self.symbol}"

class CurrencyValue(Base):
    __tablename__ = 'currency_values'

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_code: Mapped[str] = mapped_column(ForeignKey('currencies.code'))
    currency: Mapped["Currency"] = relationship(back_populates='values')
    value: Mapped[float]
    date: Mapped[datetime]


    def __repr__(self) -> str:
        return f"Currency(id={self.id}; currency_code={self.currency_code}; value={self.value}; date={self.date.isoformat()}"