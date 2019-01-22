from wtforms import Form, StringField, SubmitField, FloatField


class Converter(Form):
    weightconvert = FloatField('Convert from lbs to kg')
    heightconvert = FloatField('Convert from cm to m')
    submit = SubmitField("Update/Add your Health Information")
