from dash import Dash, html, dcc
from plotlytools import addcube
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbcode.models import Risks, Persons, Mitigations
from flask import Flask, render_template
from sqlalchemy import select




def create_risk_row(ifstatement:str,riskstatement:str,prob:int,impact:int):
    return html.Div(
        className="grid-container"
    )

#Get Risks from the database
engine = create_engine('sqlite:///dbcode/riskregister.db')
Session = sessionmaker(bind=engine)
session = Session()
risks = session.query(Risks).all()

risklist = []
for risk in risks:
    tempfig = addcube(275,risk.probability,risk.impact)
    risklist.append(html.A(risk.id,href=f'/editrisk/{risk.id}'))
    risklist.append(html.P(risk.ifstatement))
    risklist.append(html.P(risk.thenstatement))
    #Mitigations
    mitlist = []
    riskmit = session.query(Mitigations).filter(Mitigations.risk_id == risk.id).all()
    for mit in riskmit:
        if mit.complete:
            mitlist.append(html.P(mit.description,style={"text-decoration": "line-through"}))
            mitlist.append(html.P(mit.date.strftime("%Y-%m-%d"),style={"text-decoration": "line-through"}))
        else:
            mitlist.append(html.P(mit.description))
            mitlist.append(html.P(mit.date.strftime("%Y-%m-%d")))
    risklist.append(html.Div(className="mit-container", children=mitlist))
    risklist.append(dcc.Graph(figure=tempfig))

#Flask App
flask_app = Flask(__name__)

dash_app = Dash(__name__,server=flask_app,url_base_pathname='/dashboard/')



dash_app.layout = html.Div(children = [
    html.H1("Risk Register"),
    html.Div(className="grid-container", children=risklist)
])


@flask_app.route('/')
def home():
    return render_template('index.html')

@flask_app.route('/editrisk/<risk_id>', methods=['GET', 'POST'])
def edit_risk(risk_id):
    # Get the risk from the database

    risk = session.execute(select(Risks).where(Risks.id == risk_id)).scalar_one_or_none()
    if risk is None:
        return "Risk not found", 404

    # Get mitigations for the risk
    mitigations = session.execute(select(Mitigations).where(Mitigations.risk_id == risk_id)).scalars().all()

    # Render the edit risk template with the risk and mitigations data
    return render_template('riskdetail.html', risk=risk, mitigations=mitigations)

if __name__ == '__main__':
    flask_app.run(debug=True)
