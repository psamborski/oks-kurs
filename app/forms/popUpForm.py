from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Optional


class PopUpForm(FlaskForm):
    header = StringField(label='Nagłówek',
                         validators=[
                             DataRequired(message='To pole nie może być puste.'),
                             Length(min=3, max=240, message='Wprowadzony tekst powinien mieć od 3 do 240 znaków.')
                         ])
    body = TextAreaField(label='Tekst',
                         validators=[
                             DataRequired(message='To pole nie może być puste.'),
                             Length(min=5, max=1024, message='Wprowadzony tekst powinien mieć od 5 do 1024 znaków.')
                         ])
    photo = StringField(label='Link do zdjęcia (znajduje się w części Galeria; opcjonalne)',
                        validators=[
                            Optional(),
                            Length(max=240, message='Wprowadzony tekst powinien mieć do 240 znaków.')
                        ])

    show = BooleanField(label='Wyświetl pop-up na stronie głównej',
                        validators=[
                            Optional()
                        ])
