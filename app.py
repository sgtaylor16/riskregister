from dash import Dash, html, dcc
from plotlytools import addcube
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from dbcode.models import Risks, Persons, Mitigations, Programs
from flask import Flask, render_template, redirect
from flask_wtf import CSRFProtect
import secrets
from forms import RiskForm, ProgramForm


#Get Risks from the database
engine = create_engine('sqlite:///dbcode/riskregister.db')
Session = sessionmaker(bind=engine)
session = Session()
risks = session.query(Risks).all()

risklist = []
for risk in risks:
    print(risk.program)
    tempfig = addcube(275,risk.probability,risk.impact)
    risklist.append(html.A(risk.id,href=f'/editrisk/{risk.id}'))
    risklist.append(html.P(risk.ifstatement))
    risklist.append(html.P(risk.thenstatement))
    risklist.append(html.P(risk.program.name))
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

flask_app.secret_key = secrets.token_urlsafe(16)

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
    form = RiskForm(ifstatement=risk.ifstatement, thenstatement=risk.thenstatement, probability=str(risk.probability), impact=str(risk.impact))
    if form.validate_on_submit():
        # Update the risk in the database
        risk.ifstatement = form.ifstatement.data
        risk.thenstatement = form.thenstatement.data
        risk.probability = form.probability.data
        risk.impact = form.impact.data
        session.commit()

        return redirect('/')

    return render_template('riskdetail.html', risk=risk, mitigations=mitigations, form=form)

@flask_app.route('/addprograms/', methods=['GET', 'POST'])
def add_program():
    recordslist = []
    allprograms = session.query(Programs).all()
    for oneprogram in allprograms:
        recordslist.append({"id":oneprogram.id, "Program":oneprogram.name, "Description":oneprogram.description})
    form = ProgramForm()
    if form.validate_on_submit():
        # Add the program to the database
        program = Programs(name=form.name.data, description=form.description.data)
        session.add(program)
        session.commit()
        return redirect('/')

    return render_template('addprogram.html', form=form, records=recordslist)
    
if __name__ == '__main__':
    flask_app.run(debug=True)
