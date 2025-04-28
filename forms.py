from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, SubmitField, RadioField,SelectField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.fields import DateField

class RiskForm(FlaskForm):
    ifstatement = StringField('If Statement', validators=[DataRequired()])
    thenstatement = StringField('Then Statement', validators=[DataRequired()])
    probability = RadioField('Probability', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    impact = RadioField('Impact', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    submit = SubmitField('Submit')
    Program = SelectField('Program')
    Person = SelectField('Person')
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])

class ProgramForm(FlaskForm):
    name = StringField('Program Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteProgramForm(FlaskForm):
    submit = SubmitField('Delete')

class MitigationForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    probability = RadioField('Probability', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    impact = RadioField('Impact', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    date = StringField('Date (YYYY-MM-DD)')
    complete = RadioField('Complete?', choices=[('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteMitigationForm(FlaskForm):
    submit = SubmitField('Delete Mitigation')

class newRiskButton(FlaskForm):
    submit = SubmitField('New Risk',name='newrisksubmit', id='newrisksubmit')

class PersonForm(FlaskForm):
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    submit = SubmitField('Submit')