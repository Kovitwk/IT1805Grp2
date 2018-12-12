from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, SelectField, Form
from wtforms.validators import data_required, length, optional


class simData(FlaskForm):
    led = IntegerField(u'LED', validators=[data_required], default=0)
    cfl = IntegerField(u'CFL', validators=[data_required], default=0)
    inc = IntegerField(u'Incandescent', validators=[data_required], default=0)
    toish = IntegerField(u'How many bathrooms do you have?', validators=[data_required], default=1)
    toitype = SelectField(u'What type of toilets do you use?', choices=[('Old', 'Old'), ('Ultra Low Flush', 'Ultra Low Flush'), ('High Efficiency', 'High Efficiency'), ('Dual Flush', 'Dual Flush')])
    submit = SubmitField(u'Submit')









