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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def createdb():

    engine = create_engine('sqlite:///riskregister.db')
    Base.metadata.create_all(engine)


def populatedb():
    engine = create_engine('sqlite:///riskregister.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    person1 = Persons(last_name='Doe', first_name='John')
    person2 = Persons(last_name='Smith', first_name='Jane')
    session.add(person1)
    session.add(person2)
    session.commit()

    risk1 = Risks(ifstatement='If Statement #1', thenstatement='Then Statement', probability=1, impact=1, person=person1)
    risk2 = Risks(ifstatement='Risk 2',thenstatement='Then Statement2', probability=2, impact=2, person=person1)
    risk3 = Risks(ifstatement='Risk 3',thenstatement='Then Statement3',probability=3, impact=3, person=person2)
    session.add(risk1)
    session.add(risk2)
    session.add(risk3)
    session.commit()

    mitigation1 = Mitigations(description='Mitigation 1', probability=1, impact=3, risk=risk1, date=datetime.now())
    mitigation2 = Mitigations(description='Mitigation 2', probability=2, impact=4, risk=risk1, date=datetime.now())
    mitigation3 = Mitigations(description='Mitigation 3', probability=5, impact=5, risk=risk2, date=datetime.now())
    session.add(mitigation1)
    session.add(mitigation2)
    session.add(mitigation3)
    session.commit()

    

