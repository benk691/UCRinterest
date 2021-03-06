from bcrypt import hashpw, gensalt
from flask import flash
from flask.ext.wtf import Form, TextField, TextAreaField, PasswordField, SelectField, TextAreaField, SubmitField, DateTimeField, DateField, FileField, RadioField
from flask.ext.wtf import Required, Email, EqualTo, Length, file_required, file_allowed
from flask.ext.login import current_user, login_required
from werkzeug import secure_filename
from datetime import datetime
from ucri import DEFAULT_PROFILE_PIC
from ucri.models.settings import *
from permission import *

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

class SettingsForm(Form):
    '''
    Settings form for editing profiles
    '''
    fname = TextField(u'First Name', [Length(min=NAME_MIN_LENGTH, max=NAME_MAX_LENGTH)])
    lname = TextField(u'Last Name', [Length(min=NAME_MIN_LENGTH, max=NAME_MAX_LENGTH)])
    img = FileField([file_required()])
    email = TextField(u'Email address', [Email(), Length(min=EMAIL_MIN_LENGTH, max=EMAIL_MAX_LENGTH)])
    gender = SelectField(
        u'Gender',
        choices=[('M', 'Male'),
                 ('F', 'Female'),
                 ('U', 'Unspecified')]
        )
    change_pwd = SubmitField(u'Change Password')
    bday = DateField(u'Birthday (mm/dd/yyyy)', format='%m/%d/%Y')
    dscrp = TextAreaField(u'Describe yourself', [Length(min=DSCRPT_MIN_LENGTH, max=DSCRPT_MAX_LENGTH)])
    pin_browsers = SelectField(
        u'Select who can browse for your pins',
        choices=[(PERM_EVERYONE, 'Everyone'),
                 (PERM_FOLLOWERS, 'Only Your Followers'),
                 (PERM_FOLLOWING, 'Only People You Follow'), 
                 (PERM_BOTH, 'Only Followers and Following'),
                 (PERM_NOBODY, 'Nobody')]
        )
    pin_commenters = SelectField(
        u'Select who can comment on your pins',
        choices=[(PERM_EVERYONE, 'Everyone'),
                 (PERM_FOLLOWERS, 'Only Your Followers'),
                 (PERM_FOLLOWING, 'Only People You Follow'), 
                 (PERM_BOTH, 'Only Followers and Following'),
                 (PERM_NOBODY, 'Nobody')]
        )
    deactivate = SubmitField(u'Deactivate')
    save = SubmitField(u'Save Profile')

class PasswordForm(Form):
    '''
    Form for changing password
    '''
    old_pwd = PasswordField(u'Old Password')
    pwd = PasswordField(u'Password',
        [ EqualTo('confirm', message='Passwords must match'), Length(min=PWD_MIN_LENGTH, max=PWD_MAX_LENGTH) ])
    confirm = PasswordField(u'Repeat Password')
    change = SubmitField(u'Change Password')

    @login_required
    def validate(self):
        rv = Form.validate(self)
        if rv:
            if hashpw(self.old_pwd.data, current_user.pwd) == current_user.pwd:
                return True
            else:
                flash("Your old password is incorrect")
        flash("Your new password did not match with the confirmation password")
        return False

class InterestForm(Form):
    '''
    Interest form for user creation
    '''
    interest = TextField(u'Interest', [Length(min=INTEREST_MIN_LENGTH, max=INTEREST_MAX_LENGTH)])

