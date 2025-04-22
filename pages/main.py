from flask import Blueprint, render_template,redirect, request
from forms import newRiskButton, filterProgramForm
from sqlalchemy import select, func
from dbcode.models import Risks, Programs
from extensions import db

index_bp = Blueprint('index',__name__)

@index_bp.route('/')
def index():
    return render_template("index.html")

@index_bp.route('/dashboard/',methods=['GET','POST'])
def dashboard():
    newriskform = newRiskButton()

    if newriskform.validate_on_submit() and ('newrisksubmit' in request.form):
        print('In Here')
        # Handle the new risk button submission
        maxid_query = db.session.query(func.max(Risks.id)).all()
        max_id = maxid_query[0][0]+1

        return redirect(f'/editrisk/{max_id}')

    # Handle the filter program form submission
    programsselect = filterProgramForm()
    programs = db.session.execute(select(Programs)).scalars().all()
    programsselect.id.choices = [(program.id, program.name) for program in programs]
    if programsselect.validate_on_submit() and ('filterprogramsubmit' in request.form):
        print("In Program Select")
        selected_programs = programsselect.id.data
        print(selected_programs)
            

    return render_template("dashboard.html", riskbutton=newriskform, programsselect=programsselect)