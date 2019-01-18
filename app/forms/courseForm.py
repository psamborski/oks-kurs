from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, StringField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange, Length


class CourseForm(FlaskForm):
    name = StringField(label='Robocza nazwa',
                       validators=[
                           DataRequired(message='Wprowadź nazwę.'),
                           Length(max=70, message='Nazwa jest za długa.')
                       ])
    organizing_meeting_date = DateField(label='Spotkanie organizacyjne',
                                        format="%d.%m.%Y",
                                        default=datetime.today,
                                        validators=[
                                            DataRequired(message='Wprowadzona data nie jest poprawna.'),
                                        ])
    organizing_meeting_time = TimeField(label='Spotkanie organizacyjne',
                                        format="%H:%M",
                                        default=datetime.today,
                                        validators=[
                                            DataRequired(message='Wprowadzona godzina nie jest poprawna.'),
                                        ])
    start_date = DateField(label='Początek kursu',
                           format="%d.%m.%Y",
                           default=datetime.today,
                           validators=[
                               DataRequired(message='Wprowadzona data nie jest poprawna.'),
                           ])
    start_time = TimeField(label='Początek kursu',
                           format="%H:%M",
                           default=datetime.today,
                           validators=[
                               DataRequired(message='Wprowadzona godzina nie jest poprawna.'),
                           ])
    limit = IntegerField(label='Limit uczestników',
                         default=0,
                         validators=[
                             Optional(),
                             NumberRange(min=0, message='Wprowadzona liczba nie jest poprawna.')
                         ])
    cost = IntegerField(label='Koszt', default='1400',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
    additionalData = TextAreaField(label='Dodatkowe informacje widoczne przy kursie (np. inny koszt itd.)',
                                   validators=[
                                       Optional(),
                                       Length(max=120, message='Test jest za długi (120 znaków).')
                                   ])
