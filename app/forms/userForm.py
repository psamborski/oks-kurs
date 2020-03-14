from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    email = EmailField(label='Adres e-mail',
                       validators=[
                           DataRequired(message='To pole nie może być puste.'),
                           Email(message='Niepoprawny adres e-mail.')
                       ])

    bank_account = StringField(label='Numer konta',
                               validators=[
                                   DataRequired(message='To pole nie może być puste.'),
                                   Length(max=80, message='Wprowadzony tekst powinien mieć maksymalnie 80 znaków.')
                               ])
