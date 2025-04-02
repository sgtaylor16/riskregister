from flask import render_template
from app import Risks, Mitigations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import flask_app

from sqlalchemy import select

engine = create_engine('sqlite:///dbcode/riskregister.db')
Session = sessionmaker(bind=engine)
session = Session()





