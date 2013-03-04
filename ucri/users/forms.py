from flask.ext.wtf import Form, TextField, TextAreaField, PasswordField, SelectField, TextAreaField, SubmitField, DateTimeField, DateField
from flask.ext.wtf import Required, Email, EqualTo, Length
from flask.ext.login import current_user, login_required
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

class InterestForm(Form):
    '''
    Interest form for user creation
    '''
    interest = TextField(u'Interest', [Length(min=INTEREST_MIN_LENGTH, max=INTEREST_MAX_LENGTH)])

class EditForm(Form):
    '''
    Edit form for editing profiles
    '''
    # TODO: 
    #   - Think about entering your old password
    #   - If checking the current user here doesn't work then do it in the profile edit function
    def_fname = "Anonymous"
    def_lname = "NA"
    def_email = "anon@aol.com"
    def_gender = 2
    def_birthday = datetime.now()
    def_dscrp = "Description"

    if current_user != None:
        def_fname = current_user.fname
        def_lname = current_user.lname
        def_email = current_user.email
        def_gender = choices=['M', 'F', 'U'].index(current_user.gender)
        def_birthday = current_user.birthday
        def_dscrp = current_user.dscrp

    fname = TextField(u'First Name', [Length(min=NAME_MIN_LENGTH, max=NAME_MAX_LENGTH)], default=def_fname)
    lname = TextField(u'Last Name', [Length(min=NAME_MIN_LENGTH, max=NAME_MAX_LENGTH)], default=def_lname)
    email = TextField(u'Email address', [Email(), Length(min=EMAIL_MIN_LENGTH, max=EMAIL_MAX_LENGTH)], default=def_email)
    gender = SelectField(
        u'Gender',
        choices=[('M', 'Male'),
                 ('F', 'Female'),
                 ('U', 'Unspecified')],
        default=def_gender)
    pwd = PasswordField(u'Password',
        [ EqualTo('confirm', message='Passwords must match'), Length(min=PWD_MIN_LENGTH, max=PWD_MAX_LENGTH) ])
    confirm = PasswordField(u'Repeat Password')
    # Birthday
    bday = DateField(u'Birthday (mm/dd/yyyy)', format='%m/%d/%Y', default=def_birthday)
    dscrp = TextAreaField(u'Describe yourself', [Length(min=DSCRPT_MIN_LENGTH, max=DSCRPT_MAX_LENGTH)], default=def_dscrp)
    update = SubmitField(u'Update')
