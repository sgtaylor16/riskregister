from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from typing import List
from extensions import db

Base = declarative_base()
class Persons(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    last_name = Column(String(50),nullable=False)
    first_name = Column(String(50),nullable=False)
    risks = relationship("Risks",back_populates="person")

class Risks(Base):
    __tablename__ = 'risks'
    id = Column(Integer,primary_key=True)
    ifstatement = Column(String(100))
    thenstatement = Column(String(100))
    probability = Column(Integer)
    impact = Column(Integer)
    person_id = Column(ForeignKey('persons.id'),nullable=True)
    person = relationship("Persons",back_populates="risks")
    program_id = Column(ForeignKey('programs.id'))
    program = relationship("Programs",back_populates="risks")
    mitigations = relationship("Mitigations",back_populates="risk")
    date = Column(DateTime)
    realizedate = Column(DateTime,nullable=True)
    expiredate = Column(DateTime,nullable=True)
    
class Mitigations(Base):
    __tablename__ = 'mitigations'
    id = Column(Integer,primary_key=True)
    description = Column(String(100), nullable=False)
    probability = Column(Integer)
    impact = Column(Integer)
    risk_id = Column(ForeignKey('risks.id'))
    risk = relationship("Risks",back_populates="mitigations")
    date = Column(DateTime)
    complete = Column(Integer,default=0)

class Programs(Base):
    __tablename__ = 'programs'
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    risks = relationship("Risks",back_populates="program")