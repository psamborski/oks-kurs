from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    email = EmailField(label='Adres e-mail',
                       validators=[
                           DataRequired(message='To pole nie może być puste.'),
                           Email(message='Niepoprawny adres e-mail.')
                       ])
