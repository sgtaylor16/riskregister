from flask import Blueprint, render_template, redirect
from dbcode.dbtools import Risks
from extensions import db
import pandas as pd
from sqlalchemy import select

summary_bp = Blueprint('summary', __name__)

@summary_bp.route('/pigdata')
def pigcount():

    allrisks = db.session.execute(select(Risks)).scalars().all()

    countdf = pd.DataFrame(0,columns = [1,2,3,4,5],index = [1,2,3,4,5])

    for risk in allrisks:
        countdf.loc[risk.probability,risk.impact] += 1

    return countdf.to_json()

@summary_bp.route('/summary')
def summary():
    return render_template('summaries.html')



 