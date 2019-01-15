import datetime

from flask import render_template
from app import mail
from flask_mail import Message
from app.forms.signUpForm import SignUpForm
# database
from app.resources.CoursesResource import get_current_course


class Student:
    def __init__(self, signup_form):
        """
        Student attributes:
        :param signup_form:
        """
        self.signup_form = signup_form
        self.data = self.handle_form()

    def handle_form(self):
        """
        Allows to reformat sign up form to dict with nicely represented data.
        :return dict:
        """
        student_data = {'address': None}
        fields = {'name', 'surname', 'phone', 'email', 'street', 'postal', 'city', 'age'}
        address_fields = {'street', 'postal', 'city'}

        student_data['courseId'] = int(self.signup_form.courseId.data)

        for field, value in self.signup_form.data.items():
            if not value or value == 0:
                if field in fields - address_fields:
                    student_data[field] = 'brak'
                else:
                    student_data['address'] = 'brak'
            elif field in fields - address_fields:
                student_data[field] = value

        if student_data['address'] is None:
            student_data['address'] =\
                self.signup_form.street.data + ', ' \
                + self.signup_form.postal.data + ' ' \
                + self.signup_form.city.data

        return student_data
