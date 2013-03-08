from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, FileField
from flask.ext.wtf import Required, Length, file_required, file_allowed

class UploadForm(Form):
    '''
    Upload form for uploading pictures from your home directory
    '''
    title = TextField()
    photo = FileField([file_required()])
    dscrp = TextAreaField()
