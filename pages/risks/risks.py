from flask import Blueprint, render_template, redirect
from forms import RiskForm
from dbcode.models import Risks, Mitigations
from sqlalchemy import select
from app import db



risks_bp = Blueprint('risks', __name__)


@risks_bp.route('/editrisk/<risk_id>', methods=['GET', 'POST'])
def edit_risk(risk_id):
    print("i made it here")
    # Get the risk from the database

    risk = db.session.execute(select(Risks).where(Risks.id == risk_id)).scalar_one_or_none()
    if risk is None:
        return "Risk not found", 404

    # Get mitigations for the risk
    mitigations = db.session.execute(select(Mitigations).where(Mitigations.risk_id == risk_id)).scalars().all()

    # Render the edit risk template with the risk and mitigations data
    form = RiskForm(ifstatement=risk.ifstatement, thenstatement=risk.thenstatement, probability=str(risk.probability), impact=str(risk.impact))
    if form.validate_on_submit():
        # Update the risk in the database
        risk.ifstatement = form.ifstatement.data
        risk.thenstatement = form.thenstatement.data
        risk.probability = form.probability.data
        risk.impact = form.impact.data
        db.session.commit()

        return redirect('/')

    return render_template('riskdetail.html', risk=risk, mitigations=mitigations, form=form)