from wtforms import Form, StringField, validators, SubmitField


class AddRecordForm(Form):
    id = StringField('User', [validators.DataRequired()])
    height = StringField('Height in meters (e.g 1.75)', [validators.Length(min=1), validators.DataRequired()])
    weight = StringField('Weight in kilograms', [validators.Length(min=1), validators.DataRequired()])
    submit = SubmitField("Add Record")
