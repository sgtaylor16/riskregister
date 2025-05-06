from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import ForeignKey, Column
from sqlalchemy import Integer, String, DateTime
from datetime import datetime
from typing import List
from extensions import db


class Persons(db.Model):
    __tablename__ = 'persons'
    id: Mapped[int] = Column(Integer, primary_key=True)
    last_name: Mapped[str] = Column(String(50),nullable=False)
    first_name: Mapped[str] = Column(String(50),nullable=False)
    risks: Mapped[List["Risks"]] = relationship("Risks",backref="person")

class Risks(db.Model):
    __tablename__ = 'risks'
    id: Mapped[int] = Column(primary_key=True)
    ifstatement: Mapped[str] = Column(String(100))
    thenstatement: Mapped[str] = Column(String(100))
    probability: Mapped[int] = Column(Integer)
    impact: Mapped[int] = Column(Integer)
    person_id: Mapped[int] = Column(ForeignKey('persons.id'),nullable=True)
    person: Mapped['Persons'] = relationship("Persons",backref="risks")
    program_id: Mapped[int] = Column(ForeignKey('programs.id'))
    program: Mapped["Programs"] = relationship("Programs",backref="risks")
    mitigations: Mapped[List["Mitigations"]] = relationship("Mitigations",backref="risk")
    date: Mapped[datetime] = Column(DateTime)
    realizedate: Mapped[datetime] = Column(DateTime,nullable=True)
    expiredate: Mapped[datetime] = Column(DateTime,nullable=True)

class Mitigations(db.Model):
    __tablename__ = 'mitigations'
    id: Mapped[int] = Column(primary_key=True)
    description: Mapped[str] = Column(String(100), nullable=False)
    probability: Mapped[int] = Column(Integer)
    impact: Mapped[int] = Column(Integer)
    risk_id: Mapped[int] = Column(ForeignKey('risks.id'))
    risk: Mapped['Risks'] = relationship("Risks",backref="mitigations")
    date: Mapped[datetime] = Column(DateTime)
    complete: Mapped[int] = Column(default=0)

class Programs(db.Model):
    __tablename__ = 'programs'
    id: Mapped[int] = Column(primary_key=True)
    name: Mapped[str] = Column(String(100))
    description: Mapped[str] = Column(String(100))
    risks: Mapped[List["Risks"]] = relationship("Risks",backref="program")
