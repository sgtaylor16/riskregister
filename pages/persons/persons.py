from flask import Blueprint, render_template, redirect, flash
from forms import PersonForm, DeletePersonForm
from dbcode.models import Persons, Risks,Mitigations
from extensions import db
persons_bp = Blueprint('persons', __name__)

@persons_bp.route('/addpersons/', methods=['GET', 'POST'])
def add_person():
    recordslist = []
    allpersons = db.session.query(Persons).all()
    for oneperson in allpersons:
        recordslist.append({"id":oneperson.id,
                             "first_name":oneperson.first_name,
                             "last_name":oneperson.last_name
                             })
    # Create a form instance
    form = PersonForm()
    if form.validate_on_submit():
        # Add the person to the database
        person = Persons(first_name=form.first_name.data, last_name =form.last_name.data)
        db.session.add(person)
        db.session.commit()
        return redirect('/addpersons')
    
    return render_template('addperson.html', form=form, records=recordslist)
    
@persons_bp.route('/editperson/<int:person_id>', methods=['GET', 'POST'])
def edit_person(person_id):
    recordslist = []
    allpersons = db.session.query(Persons).all()
    modperson = db.session.query(Persons).filter(Persons.id == person_id).first()
    for oneperson in allpersons:
        recordslist.append({"id":oneperson.id,
                             "first_name":oneperson.first_name,
                             "last_name":oneperson.last_name
                             })
    # Create a form instance
    form = PersonForm(first_name=modperson.first_name, last_name=modperson.last_name)
    if form.validate_on_submit():
        # Update the person in the database
        modperson.first_name = form.first_name.data
        modperson.last_name = form.last_name.data
        db.session.commit()
        return redirect('/addpersons')
        
    return render_template('addperson.html', form=form, records=recordslist)

@persons_bp.route('/deleteperson/<int:person_id>', methods=['GET', 'POST'])
def delete_person(person_id):
    personcheck = db.session.query(Persons).filter(Persons.id == person_id).first().risks
    if len(personcheck) > 0:
        flash("Person has associated risks. Cannot delete.")
        return redirect('/addpersons/')
    else:
        person = db.session.query(Persons).filter(Persons.id == person_id).first()
        db.session.delete(person)
        db.session.commit()
        return redirect('/addpersons/')