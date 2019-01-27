from wtforms import *


class AddRecordForm(Form):
    id = StringField('User', [validators.DataRequired()])
    height = StringField('Height in m (e.g 1.75)', [validators.Length(min=4, max=4), validators.DataRequired()])
    weight = StringField('Weight in kg (e.g 75)', [validators.Length(min=1), validators.DataRequired()])
    submit = SubmitField("Update/Add your Health Information")
    weightconvert = FloatField('Convert from lbs to kg')
    heightconvert = FloatField('Convert from cm to m')
