from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



class CAddJointForm(FlaskForm):
    x = StringField('x coord', validators=[DataRequired()])
    y = StringField('y coord', validators=[DataRequired()])
    z = StringField('z coord', validators=[DataRequired()])
    submit = SubmitField('Add Joint')