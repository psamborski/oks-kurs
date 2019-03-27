from flask_wtf import FlaskForm
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, NumberRange


class PricesForm(FlaskForm):
    course_price = IntegerField(label='Koszt kursu',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
    driving_lesson_kurs = IntegerField(label='Koszt jednej lekcji (OSK Kurs)',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
    driving_lesson_stranger = IntegerField(label='Koszt jednej lekcji (osoba z zewnątrz)',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
    driving_lesson_10_kurs = IntegerField(label='Pakiet 10 godzin jazd (OSK Kurs)',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
    driving_lesson_10_stranger = IntegerField(label='Pakiet 10 godzin jazd (osoba z zewnątrz)',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
    driving_lesson_20_kurs = IntegerField(label='Pakiet 20 godzin jazd (OSK Kurs)',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
    driving_lesson_20_stranger = IntegerField(label='Pakiet 20 godzin jazd (OSK Kurs)',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
    driving_lesson_30_kurs = IntegerField(label='Pakiet 30 godzin jazd (OSK Kurs)',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
    driving_lesson_30_stranger = IntegerField(label='Pakiet 30 godzin jazd (OSK Kurs)',
                        validators=[
                            DataRequired(message='Wprowadzona cena nie jest poprawna.'),
                            NumberRange(min=0, message='Podana wartość nie jest liczbą')
                        ])
