from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SubmitField, RadioField,SelectField
from wtforms.validators import DataRequired

class RiskForm(FlaskForm):
    ifstatement = StringField('If Statement', validators=[DataRequired()])
    thenstatement = StringField('Then Statement', validators=[DataRequired()])
    probability = RadioField('Probability', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    impact = RadioField('Impact', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    submit = SubmitField('Submit')
    Program = SelectField('Program')

class ProgramForm(FlaskForm):
    name = StringField('Program Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteProgramForm(FlaskForm):
    program_id = SelectField('Program ID', validators=[DataRequired()])
    submit = SubmitField('Delete Program')

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
    submit = SubmitField('New Risk')