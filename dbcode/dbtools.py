from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String, DateTime
from datetime import datetime
from dbcode.models import Persons, Risks, Mitigations, Programs
from extensions import db


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def createdb():

    engine = create_engine('sqlite:///dbcode/riskregister.db')
    db.metadata.create_all(engine)


def populatedb():
    engine = create_engine('sqlite:///dbcode/riskregister.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    person1 = Persons(last_name='Doe', first_name='John')
    person2 = Persons(last_name='Smith', first_name='Jane')
    session.add(person1)
    session.add(person2)
    session.commit()

    program1 = Programs(name='Program 1', description='Description 1')
    program2 = Programs(name='Program 2', description='Description 2')
    session.add(program1)
    session.add(program2)
    session.commit()

    risk1 = Risks(ifstatement='If Statement #1', thenstatement='Then Statement', probability=1, impact=1, person=person1,program=program1)
    risk2 = Risks(ifstatement='Risk 2',thenstatement='Then Statement2', probability=2, impact=2, person=person1,program=program2)
    risk3 = Risks(ifstatement='Risk 3',thenstatement='Then Statement3',probability=3, impact=3, person=person2,program=program1)
    session.add(risk1)
    session.add(risk2)
    session.add(risk3)
    session.commit()

    mitigation1 = Mitigations(description='Mitigation 1', probability=1, impact=3, risk=risk1, date=datetime.now())
    mitigation2 = Mitigations(description='Mitigation 2', probability=2, impact=4, risk=risk1, date=datetime.now(),complete=True)
    mitigation3 = Mitigations(description='Mitigation 3', probability=5, impact=5, risk=risk2, date=datetime.now())
    session.add(mitigation1)
    session.add(mitigation2)
    session.add(mitigation3)
    session.commit()

    session.close()
    

