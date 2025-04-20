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
        return redirect('/')
    
    deleteForm = DeletePersonForm()
    deleteForm.person_id.choices = [(person.id, person.first_name) for person in allpersons]
    if deleteForm.validate_on_submit():
        # Delete the person from the database
        person_id = deleteForm.person_id.data
        person = db.session.query(Persons).filter(Persons.id == person_id).first()
        
        personcheck = db.session.query(Risks).filter(Risks.person_id == person_id).all()
        mitigationcheck = db.session.query(Mitigations).filter(Mitigations.person_id == person_id).all()
        if personcheck is not None:
            flash("Cannot delete person with associated risks.")
            return redirect('/addpersons/')
        elif mitigationcheck is not None :
            flash("Cannot delete person with associated mitigations.")
            return redirect('/addpersons/')
        else:
            # Delete the person if it exists
            if person:
                db.session.delete(person)
                db.session.commit()
        return redirect('/')
        
    
    return render_template('addperson.html', form=form,deleteform =deleteForm, records=recordslist)