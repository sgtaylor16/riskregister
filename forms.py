from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, SubmitField, RadioField,SelectField, Form
from wtforms.validators import DataRequired
from wtforms.fields import DateField
from flask import request

class BaseForm(Form):
    def validate_on_submit(self):
        return request.method =="POST" and self.validate()

class RiskForm(BaseForm):
    ifstatement = StringField('If Statement', validators=[DataRequired()])
    thenstatement = StringField('Then Statement', validators=[DataRequired()])
    probability = RadioField('Probability', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    impact = RadioField('Impact', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    submit = SubmitField('Submit')
    Program = SelectField('Program')
    Person = SelectField('Person')
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    realizedate = DateField('Realization Date', format='%Y-%m-%d')
    expiredate = DateField('Expiration Date', format='%Y-%m-%d')

class ProgramForm(BaseForm):
    name = StringField('Program Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteProgramForm(BaseForm):
    submit = SubmitField('Delete')

class MitigationForm(BaseForm):
    description = StringField('Description', validators=[DataRequired()])
    probability = RadioField('Probability', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    impact = RadioField('Impact', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    complete = RadioField('Complete?', choices=[('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteMitigationForm(BaseForm):
    submit = SubmitField('Delete Mitigation')

class newRiskButton(BaseForm):
    submit = SubmitField('New Risk',name='newrisksubmit', id='newrisksubmit')

class PersonForm(BaseForm):
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    submit = SubmitField('Submit')