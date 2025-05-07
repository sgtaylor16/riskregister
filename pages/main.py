from flask import Blueprint, render_template,redirect, request
from forms import newRiskButton
from sqlalchemy import select, func
from dbcode.models import Risks, Programs, Persons
from extensions import db

index_bp = Blueprint('index',__name__)

@index_bp.route('/')
def index():
    return render_template("index.html")

@index_bp.route('/dashboard/',methods=['GET','POST'])
def dashboard():
    newriskform = newRiskButton()
    programs = db.session.execute(select(Programs)).scalars().all()
    selected_programs =  [(program.id, program.name) for program in programs]

    persons = db.session.execute(select(Persons)).scalars().all()
    selected_persons =  [(person.id, person.last_name + ', ' + person.first_name) for person in persons]
    if newriskform.validate_on_submit():
        # Handle the new risk button submission
        maxid_query = db.session.query(func.max(Risks.id)).all()
        max_id = maxid_query[0][0]+1

        return redirect(f'/editrisk/{max_id}')

        
    return render_template("dashboard.html", riskbutton=newriskform, selected_programs=selected_programs,selected_persons=selected_persons)