from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, FileField
from flask.ext.wtf import Required, Length, file_required, file_allowed

class UploadForm(Form):
    title = TextField()
    photo = FileField([file_required()])
    dscrp = TextAreaField()
