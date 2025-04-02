from flask import Blueprint, render_template, redirect, flash
from forms import ProgramForm, DeleteProgramForm
from dbcode.models import Programs, Risks
from sqlalchemy import select
from app import db
programs_bp = Blueprint('programs', __name__)


@programs_bp.route('/addprograms/', methods=['GET', 'POST'])
def add_program():
    recordslist = []
    allprograms = session.query(Programs).all()
    for oneprogram in allprograms:
        recordslist.append({"id":oneprogram.id, "Program":oneprogram.name, "Description":oneprogram.description})
    form = ProgramForm()
    if form.validate_on_submit():
        # Add the program to the database
        program = Programs(name=form.name.data, description=form.description.data)
        db.session.add(program)
        db.session.commit()
        return redirect('/')
    
    deleteForm = DeleteProgramForm()
    deleteForm.program_id.choices = [(program.id, program.name) for program in allprograms]
    if deleteForm.validate_on_submit():
        # Delete the program from the database
        program_id = deleteForm.program_id.data
        program = db.session.query(Programs).filter(Programs.id == program_id).first()
        
        riskscheck = db.session.query(Risks).filter(Risks.program_id == program_id).all()
        if riskscheck:
            flash("Cannot delete program with associated risks.")
            return redirect('/addprograms/')
        # Delete the program if it exists
        if program:
            db.session.delete(program)
            db.session.commit()
        return redirect('/')

    return render_template('addprogram.html', form=form ,deleteform=deleteForm, records=recordslist)