from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, BooleanField, RadioField
from wtforms.fields.html5 import EmailField, TelField, IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional, NumberRange

from app.models.functions import prepare_courses_for_radio


class SignUpForm(FlaskForm):
    courseId = RadioField(label='Kurs', coerce=int,
                          # https://stackoverflow.com/questions/13964152/not-a-valid-choice-for-dynamic-select-field-wtforms
                          validators=[
                              DataRequired()
                          ]
                          )
    name = StringField(label='Imię',
                       validators=[
                           DataRequired(message='To pole nie może być puste.'),
                           Length(min=2, max=20, message='Wprowadzony tekst powinien mieć od 2 do 20 znaków.')
                       ])
    surname = StringField(label='Nazwisko',
                          validators=[
                              DataRequired(message='To pole nie może być puste.'),
                              Length(min=2, max=40, message='Wprowadzony tekst powinien mieć od 2 do 40 znaków.')
                          ])
    email = EmailField(label='Adres e-mail',
                       validators=[
                           DataRequired(message='To pole nie może być puste.'),
                           Email(message='Niepoprawny adres e-mail.')
                       ])
    phone = TelField(label='Numer telefonu',
                     validators=[
                         DataRequired(message='To pole nie może być puste.'),
                         Regexp(r'(?<!\w)(\(?(\+)?\d{2}\)?)?[ -]?\d{3}[ -]?((\d{3}[ -]?\d{3})|(\d{2}[ -]?\d{2}))(?!\w)',
                                message='To pole nie zawiera poprawnego numeru telefonu.')
                     ])
    street = StringField(label='Ulica',
                         validators=[
                             Optional(),
                             Length(max=40, message='Wprowadzony tekst powinien mieć maksymalnie 40 znaków.')
                         ])
    city = StringField(label='Miasto',
                       validators=[
                           Optional(),
                           Length(max=40, message='Wprowadzony tekst powinien mieć maksymalnie 40 znaków.')
                       ])
    postal = StringField(label='Kod pocztowy',
                         validators=[
                             Optional(),
                             Regexp(r'((?<!\w)(\d{2})[-]\d{3}(?!\w))',
                                    message='To pole nie zawiera poprawnego kodu pocztowego. '
                                            'Wprowadź poprawny lub pozostaw pole puste.')
                         ])
    age = IntegerRangeField(label='Wiek', default=0,
                            validators=[
                                NumberRange(min=0, max=100)
                            ])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Zaznacz to pole i uzupełnij wymagane dane.')])
    data_agreement = BooleanField(label='Wyrażam zgodę na przetwarzanie moich danych osobowych.',
                                  validators=[
                                      DataRequired(message='Musisz wyrazić zgodę na przetwarzanie danych.')
                                  ])

    @classmethod
    def update_form(cls):
        """
         At first, this thing was written and executed directly in the form but form has to refresh data
         after course data edit and update. Calling this function allows to do it.

        :return sign up form:
        """
        # Get closest courses from function
        three_closest_courses = prepare_courses_for_radio()

        # Instantiate the form; I have to pass default here
        form = cls(courseId=three_closest_courses[0][0] if three_closest_courses else None)

        # Set the choices for the course field
        form.courseId.choices = three_closest_courses

        return form
