from flask.ext.wtf import Form, TextField
from flask.ext.wtf import Required

class LoginForm(Form):
	name = TextField('name', validators = [Required()])
	password = TextField('password')
