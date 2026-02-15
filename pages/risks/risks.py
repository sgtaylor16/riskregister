from flask import Blueprint, render_template, redirect, jsonify, request
from forms import RiskForm,MitigationForm,DeleteMitigationForm
from dbcode.models import Risks, Mitigations, Programs,Persons
from sqlalchemy import select, and_
from extensions import db
from dateutil.parser import parse
from typing import List, Dict
from misctools import score


risks_bp = Blueprint('risks', __name__)


@risks_bp.route('/editrisk/<risk_id>', methods=['GET', 'POST'])
def edit_risk(risk_id):
    # Find the maximum risk ID in the database
    max_risk_id = db.session.query(db.func.max(Risks.id)).scalar()
    if max_risk_id is None:
        max_risk_id = 0
    else:
        max_risk_id = int(max_risk_id)

    if int(risk_id) <= max_risk_id:
    #It is an existing risk get it.

        risk = db.session.execute(select(Risks).where(Risks.id == risk_id)).scalar_one_or_none()
        if risk is None:
            return "Risk not found", 404
        
        #Get the associated program
        riskprogram = Programs.query.filter_by(id=risk.program_id).first()
        riskperson = Persons.query.filter_by(id=risk.person_id).first()

        form = RiskForm(ifstatement=risk.ifstatement,
                        thenstatement=risk.thenstatement,
                        probability=str(risk.probability),
                        impact=str(risk.impact), 
                        Program=riskprogram.id,
                        Person=riskperson.id,
                        date=risk.date,
                        realizedate=risk.realizedate,
                        expiredate=risk.expiredate)

        if len(Programs.query.all()) > 0:
            form.Program.choices = sorted([(program.id, program.name) for program in Programs.query.all()])

        if len(Persons.query.all()) > 0:
            form.Person.choices = sorted([(person.id,person.last_name + " " + person.first_name) for person in Persons.query.all()])

        if form.validate_on_submit():
            # Update the risk in the database
            risk.ifstatement = form.ifstatement.data
            risk.thenstatement = form.thenstatement.data
            risk.probability = form.probability.data
            risk.impact = form.impact.data
            risk.program_id = form.Program.data
            risk.person_id = form.Person.data
            risk.date = form.date.data
            risk.realizedate = form.realizedate.data
            risk.expiredate = form.expiredate.data

            db.session.commit()

            return redirect('/')

        return render_template('riskdetail.html', form=form)
    else:
    #It is a new risk

        form= RiskForm()

        if (Programs.query.all() is not None):
            form.Program.choices = sorted([(program.id, program.name) for program in Programs.query.all()])
    
        if len(Persons.query.all()) > 0:
            form.Person.choices = sorted([(person.id,person.last_name + " " + person.first_name) for person in Persons.query.all()])

        if form.validate_on_submit():
            print("Form validated")
            
            # Create a new risk in the database

            # Add checks to realizedate and expiredate

            newrisk = Risks(ifstatement=form.ifstatement.data,
                            thenstatement=form.thenstatement.data, 
                            probability=form.probability.data,
                            impact=form.impact.data,
                            person_id=form.Person.data,
                            program_id=form.Program.data,
                            date=form.date.data,
                            realizedate=form.realizedate.data,
                            expiredate=form.expiredate.data
                            )
            print(newrisk)
            
            db.session.add(newrisk)
            db.session.commit()

            return redirect('/')
        else:
            #Should only get here if the form did not validate
            print(form.errors)
        
        return render_template('riskdetail.html', form=form)


def buildrisklist(risks: List[Risks]) -> List[Dict]:
    # This function will be called to build the list of risks for the risk dashboard
    # It takes a list of risks and returns a list of dictionaries with the risk data
    listofrisks = []
    for risk in risks:
        newob = {}
        newob['id'] = risk.id
        newob['ifstatement'] = risk.ifstatement
        newob['thenstatement'] = risk.thenstatement
        newob['probability'] = risk.probability
        newob['program'] = risk.program.name
        newob['impact'] = risk.impact
        newob['person'] = risk.person.last_name + ", " + risk.person.first_name
        newob['score'] = score(risk.probability,risk.impact)
        mitigationlist = []
        for mitigation in risk.mitigations:
            mitigationlist.append({
                'id': mitigation.id,
                'description': mitigation.description,
                'probability': mitigation.probability,
                'impact': mitigation.impact,
                'date': mitigation.date.strftime('%Y-%m-%d'),
                'complete': mitigation.complete
            })
        # Sort the mitigation list by date
        mitigationlist.sort(key=lambda x: x['date'])
        newob['mitigations'] = mitigationlist

        listofrisks.append(newob)
    # Sort the list of risks by score
    listofrisks.sort(key=lambda x: x['score'], reverse=True)
    return listofrisks

@risks_bp.route('/riskdata', methods=['POST','GET'])
def risk_dashboard():

    if request.method== 'GET':
        # This route function will be called via fetch when the user accesses the risk dashboard
        risks = db.session.execute(select(Risks)).scalars().all()
        listofrisks = buildrisklist(risks)
    else:

        newselected_prog = request.get_json()['programs']
        newselected_persons = request.get_json()['persons']
        listofrisks = []

        risks =db.session.execute(select(Risks).where(and_(Risks.program_id.in_(newselected_prog),Risks.person_id.in_(newselected_persons)))).scalars().all()
        listofrisks = buildrisklist(risks)
    
    return jsonify(listofrisks)

@risks_bp.route('/editmit/<mitigation_id>', methods=['GET', 'POST'])
def edit_mitigation(mitigation_id):
    # Get the mitigation from the database
    mitigation = db.session.execute(select(Mitigations).where(Mitigations.id == mitigation_id)).scalar_one_or_none()
    if mitigation is None:
        return "Mitigation not found", 404

    # Render the edit risk template with the risk and mitigations data
    mitform = MitigationForm(description=mitigation.description, probability=str(mitigation.probability), impact=str(mitigation.impact), date=mitigation.date, complete=str(mitigation.complete))
    if mitform.validate_on_submit():
        # Update the mitigation in the database
        mitigation.description = mitform.description.data
        mitigation.probability = mitform.probability.data
        mitigation.impact = mitform.impact.data
        mitigation.date = mitform.date.data
        mitigation.complete = mitform.complete.data
        db.session.commit()

        return redirect('/dashboard')
    
    deletemitform = DeleteMitigationForm()
    if deletemitform.validate_on_submit():
        # Delete the mitigation from the database
        print("Deleting mitigation")
        return redirect('/deletemit/' + str(mitigation_id))
    else:
        print(deletemitform.errors)

    return render_template('editmitigation.html',mitform=mitform, deletemitform=deletemitform, mitigation_id=mitigation_id)

@risks_bp.route('/deletemit/<mitigation_id>', methods=['POST'])
def delete_mitigation(mitigation_id):
    # Get the mitigation from the database
    mitigation = db.session.execute(select(Mitigations).where(Mitigations.id == mitigation_id)).scalar_one_or_none()
    if mitigation is None:
        return "Mitigation not found", 404

    # Delete the mitigation from the database
    db.session.delete(mitigation)
    db.session.commit()

    return redirect('/dashboard')

@risks_bp.route('/newmit/<risk_id>', methods=['GET', 'POST'])
def new_mitigation(risk_id):
    # Get the risk from the database
    risk = db.session.execute(select(Risks).where(Risks.id == risk_id)).scalar_one_or_none()
    if risk is None:
        return "Risk not found", 404

    if request.method == 'POST':
        # Create a new mitigation in the database
        newmitigation = Mitigations(description=request.form.get('description'),
                                     probability=int(request.form.get('probability')),
                                     impact=int(request.form.get('impact')),
                                     date=parse(request.form.get('date')),
                                     complete=int(request.form.get('complete')))
        risk.mitigations.append(newmitigation)
        db.session.commit()

        return redirect('/')

    return render_template('newmitigation.html')

@risks_bp.route('/deleterisk/<risk_id>', methods=['POST'])
def delete_risk(risk_id):
    # Get the risk from the database
    risk = db.session.execute(select(Risks).where(Risks.id == risk_id)).scalar_one_or_none()
    if risk is None:
        return "Risk not found", 404

    # Delete the risk from the database
    db.session.delete(risk)
    db.session.commit()

    # Delete mitigations associated with the risk
    mitigations = db.session.execute(select(Mitigations).where(Mitigations.risk_id == risk_id)).scalars().all()
    for mitigation in mitigations:
        db.session.delete(mitigation)
    db.session.commit()

    return redirect('/dashboard')