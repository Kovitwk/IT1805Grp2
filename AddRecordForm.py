from wtforms import Form, StringField, validators, SubmitField


class AddRecordForm(Form):
    height = StringField('Height in meters (e.g 1.75)', [validators.Length(min=1, max=3), validators.DataRequired()])
    weight = StringField('Weight in kilograms', [validators.Length(min=1, max=3), validators.DataRequired()])
    submit = SubmitField("Add Record")
