from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy import Integer, String, DateTime
from datetime import datetime
from typing import List
from extensions import db

class Persons(db.Model):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    last_name = Column(String(50),nullable=False)
    first_name = Column(String(50),nullable=False)
    risks = relationship("Risks",back_populates="person")

class Risks(db.Model):
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
    
class Mitigations(db.Model):
    __tablename__ = 'mitigations'
    id = Column(Integer,primary_key=True)
    description = Column(String(100), nullable=False)
    probability = Column(Integer)
    impact = Column(Integer)
    risk_id = Column(ForeignKey('risks.id'))
    risk = relationship("Risks",back_populates="mitigations")
    date = Column(DateTime)
    complete = Column(Integer,default=0)

class Programs(db.Model):
    __tablename__ = 'programs'
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    risks = relationship("Risks",back_populates="program")