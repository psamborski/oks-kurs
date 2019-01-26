import re


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
                elif field in address_fields:
                    student_data['address'] = 'brak'
            elif value and field in fields - address_fields:
                student_data[field] = value

        if student_data['address'] is None:
            student_data['address'] =\
                self.signup_form.street.data + ', ' \
                + self.signup_form.postal.data + ' ' \
                + self.signup_form.city.data

        student_data['phone'] = re.sub("[^0-9|+]", "", student_data['phone'])  # remove all non-numeric characters

        return student_data
