from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GradeForm(FlaskForm):
    assignment = StringField('Assignment', validators=[DataRequired()])
    score = StringField('Score', validators=[DataRequired()])
    max_score = StringField('Maximum Possible Score', validators=[DataRequired()])
    submit = SubmitField('Add Changes')