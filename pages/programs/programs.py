from flask import Blueprint, render_template, redirect, flash
from forms import ProgramForm, DeleteProgramForm
from dbcode.models import Programs, Risks
from sqlalchemy import select
from extensions import db
programs_bp = Blueprint('programs', __name__)


@programs_bp.route('/addprograms/', methods=['GET', 'POST'])
def add_program():
    recordslist = []
    allprograms = db.session.query(Programs).all()
    for oneprogram in allprograms:
        recordslist.append({"id":oneprogram.id, "Program":oneprogram.name, "Description":oneprogram.description})
    form = ProgramForm()
    if form.validate_on_submit():
        # Add the program to the database
        program = Programs(name=form.name.data, description=form.description.data)
        db.session.add(program)
        db.session.commit()
        return redirect('/addprograms')

    return render_template('addprogram.html', form=form,  records=recordslist)

@programs_bp.route('/editprogram/<int:program_id>', methods=['GET', 'POST'])
def edit_program(program_id):
    recordslist = []
    allprograms = db.session.query(Programs).all()
    modprogram = db.session.query(Programs).filter(Programs.id == program_id).first()
    for oneprogram in allprograms:
        recordslist.append({"id":oneprogram.id, "Program":oneprogram.name, "Description":oneprogram.description})
    form = ProgramForm(name=modprogram.name, description=modprogram.description)
    if form.validate_on_submit():
        # Update the program in the database
        modprogram.name = form.name.data
        modprogram.description = form.description.data
        db.session.commit()
        return redirect('/addprograms')
    return render_template('addprogram.html', form=form, records=recordslist)

@programs_bp.route('/deleteprogram/<int:program_id>', methods=['GET', 'POST'])
def delete_program(program_id):
    programcheck = db.session.query(Programs).filter(Programs.id == program_id).first().risks
    if len(programcheck) > 0:
        flash("Program has associated risks. Cannot delete.")
        return redirect('/addprograms/')
    else:
        program = db.session.query(Programs).filter(Programs.id == program_id).first()
        db.session.delete(program)
        db.session.commit()
        return redirect('/addprograms/')