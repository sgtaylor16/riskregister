from flask import Blueprint, render_template,redirect
from forms import newRiskButton
from sqlalchemy import select, func
from dbcode.models import Risks
from extensions import db

index_bp = Blueprint('index',__name__)

@index_bp.route('/')
def index():
    return render_template("index.html")

@index_bp.route('/dashboard/',methods=['GET','POST'])
def dashboard():
    newriskform = newRiskButton()
    if newriskform.is_submitted():
        # Handle the new risk button submission
        maxid_query = db.session.query(func.max(Risks.id)).all()
        max_id = maxid_query[0][0]+1
        #max_id = int(maxid_query.scalar()) + 1
        #print(max_id)

        return redirect(f'/editrisk/{max_id}')    

    return render_template("dashboard.html", riskbutton=newriskform)