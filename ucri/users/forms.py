from flask.ext.wtf import Form, TextField, TextAreaField, PasswordField, SelectField, TextAreaField, SubmitField, DateTimeField, DateField
from flask.ext.wtf import Required, Email, EqualTo, Length
from datetime import datetime
from ucri.models.settings import *

class RegisterForm(Form):
    '''
    Register form for user creation
    '''
    fname = TextField(u'First Name', [Required(), Length(min=NAME_MIN_LENGTH, max=NAME_MAX_LENGTH)])
    lname = TextField(u'Last Name', [Required(), Length(min=NAME_MIN_LENGTH, max=NAME_MAX_LENGTH)])
    uname = TextField(u'User Name', [Required(), Length(min=NAME_MIN_LENGTH, max=NAME_MAX_LENGTH)])
    email = TextField(u'Email address', [Required(), Email(), Length(min=EMAIL_MIN_LENGTH, max=EMAIL_MAX_LENGTH)])
    gender = SelectField(
        u'Gender', [Required()],
        choices=[('M', 'Male'),
                 ('F', 'Female'),
                 ('U', 'Unspecified')]
        )
    pwd = PasswordField(u'Password',
        [ Required(), EqualTo('confirm', message='Passwords must match'), Length(min=PWD_MIN_LENGTH, max=PWD_MAX_LENGTH) ])
    confirm = PasswordField(u'Repeat Password', [Required()])
    # Birthday
    bday = DateField(u'Birthday (mm/dd/yyyy)', format='%m/%d/%Y', default=datetime(1970, 1, 1))
    dscrp = TextAreaField(u'Describe yourself', [Length(min=DSCRPT_MIN_LENGTH, max=DSCRPT_MAX_LENGTH)])
    reg = SubmitField(u'Register')

"""
class InterestForm(Form):
    '''
    Interest form for user creation
    '''
    interest = TextField(u'Interest', [Length(min=INTEREST_MIN_LENGTH, max=INTEREST_MAX_LENGTH)])
"""
