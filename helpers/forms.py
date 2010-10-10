from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, SelectField, validators

class LoginAccountForm(Form): 
    username = TextField('username', [validators.Required(message='no user name provided!')])
    password = PasswordField('password', [validators.Required(message='no password provided!')])

class CreateAccountForm(Form):
    username = TextField('username', [validators.Required(message='you need a user name right?')])
    password = PasswordField('password', [validators.Required(message='you need a password right?')])

class ChooseOccup(Form):
    occupation = SelectField('occupation', choices=[('merchant', 'Merchant'), ('mercernary', 'Mercenary'), ('pwet', 'Martie')])

class AddJob(Form): 
    job_name = TextField('job_nm', [validators.Required(message='no job name provided!')])
    job_desc = TextAreaField('job_desc', [validators.Required(message='no job description provided!')])

