from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String, DateTime
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

class Persons(Base):
    __tablename__ = 'persons'
    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    risks: Mapped[List["Risks"]] = relationship(back_populates="person")

class Risks(Base):
    __tablename__ = 'risks'
    id: Mapped[int] = mapped_column(primary_key=True)
    ifstatement: Mapped[str] = mapped_column(String(100))
    thenstatement: Mapped[str] = mapped_column(String(100))
    probability: Mapped[int] = mapped_column(Integer)
    impact: Mapped[int] = mapped_column(Integer)
    person_id: Mapped[int] = mapped_column(ForeignKey('persons.id'))
    person: Mapped['Persons'] = relationship(back_populates="risks")
    program_id: Mapped[int] = mapped_column(ForeignKey('programs.id'))
    program: Mapped["Programs"] = relationship(back_populates="risk")
    mitigations: Mapped[List["Mitigations"]] = relationship(back_populates="risk")

class Mitigations(Base):
    __tablename__ = 'mitigations'
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))
    probability: Mapped[int] = mapped_column(Integer)
    impact: Mapped[int] = mapped_column(Integer)
    risk_id: Mapped[int] = mapped_column(ForeignKey('risks.id'))
    risk: Mapped['Risks'] = relationship(back_populates="mitigations")
    date: Mapped[datetime] = mapped_column(DateTime)
    complete: Mapped[bool] = mapped_column(default=False)

class Programs(Base):
    __tablename__ = 'programs'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    risk: Mapped["Risks"] = relationship(back_populates="program")
