from flask import Blueprint, render_template
from forms import newRiskButton

index_bp = Blueprint('index',__name__)

@index_bp.route('/')
def index():
    return render_template("index.html")

@index_bp.route('/dashboard/')
def dashboard():
    riskbutton = newRiskButton()
    return render_template("dashboard.html", riskbutton=riskbutton)