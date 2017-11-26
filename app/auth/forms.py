# Import Form and RecaptchaField (optional)
from flask_wtf import Form, RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class LoginForm(Form):
    email      = TextField     ('Email Address')
    password   = PasswordField ('Password')
    rememberme = BooleanField  ('Remember me')
    recaptcha  = RecaptchaField()
    autofocus  = 'email'
