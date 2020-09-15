from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired()])
    submit = SubmitField('Finish Changes')
