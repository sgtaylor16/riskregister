from flask import Blueprint, render_template, jsonify, request
from dbcode.dbtools import Risks, Mitigations
from extensions import db
import pandas as pd
from sqlalchemy import select
from misctools import score


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

@summary_bp.route('/waterfall/<risk_id>',methods=['GET', 'POST'])
def waterfall(risk_id):

    return render_template('riskwaterfall.html', id = risk_id)

@summary_bp.route('/riskwaterfalldata/<risk_id>',methods=['GET'])
def waterfalldata(risk_id):
    wflist = []
    risk = db.session.execute(select(Risks).where(Risks.id == risk_id)).scalar_one_or_none()
    startprob = risk.probability
    startimpact = risk.impact
    startdate = risk.date
    wflist.append({'date': startdate, 'probability': startprob, 'impact': startimpact,'complete': 0,'score': score(startprob,startimpact)})
    mitigations = db.session.execute(select(Mitigations).where(Mitigations.risk_id == risk_id)).scalars().all()
    for mitigation in mitigations:
        wflist.append({'date': mitigation.date,
                       'probability': mitigation.probability,
                       'impact': mitigation.impact,
                       'complete': mitigation.complete,
                       'score': score(mitigation.probability,mitigation.impact)})
    return jsonify(wflist)

@summary_bp.route('progwaterfalldata',methods=['GET','PUT'])
def progwaterfalldata():

    startdate = request.args.get('startdate')

    #Get all the risks
    allrisks = db.session.execute(select(Risks)).scalars().all()


 