from flask import render_template
from flask_mail import Message

from app import mail
# database
from app.models.StudentModel import Student
from app.resources.UsersResource import get_admin_mail


class Mail:
    def __init__(self, topic, content, recipients=None, reply_email='noreply@osk-kurs.pl', mail_type=None):
        """
        Mail attributes:
        :param topic:
        :param content: String or sign up form.
        :param recipients:
        :param reply_email:
        :param mail_type: Basic (default) email with no template (None), confirm email or notification email.
        """

        # Check if recipient is given and if so - check if the type is correct. Otherwise, set to default.
        if recipients is None:
            recipients = [get_admin_mail()]
            # recipients = ["psambek@osk-kurs.pl"]
        elif type(recipients) is not list:
            if type(recipients) is str:
                recipients = [recipients]
            else:
                recipients = [get_admin_mail()]
                # recipients = ["psambek@osk-kurs.pl"]

        self.topic = topic
        self.recipients = recipients
        self.reply_email = reply_email
        self.mail_type = mail_type

        if isinstance(content, tuple) and (self.mail_type == 'confirm' or self.mail_type == 'notification'):
            # if form and type is correct as well, build a message from template
            self.content = self.build_message(content)
        else:
            self.content = self.reformat_message(content)

    @staticmethod
    def reformat_message(content):
        """
        Replaces new line signs to html types.

        :return: New content.
        """
        return content.replace('\r\n', "<br>")

    def build_message(self, content):
        """
        Build a message containing sign up form data - confirm mail for student or notification mail for teacher/admin.

        :param content:
        :return: email template
        """
        student_data = Student(content[0]).data  # form

        if self.mail_type == 'confirm':
            return render_template('confirm-email.html', student_data=student_data, date=content[1])  # date
        elif self.mail_type == 'notification':
            return render_template('notification-email.html', student_data=student_data, date=content[1])

    def send(self):
        """
        Sends a message.
        """
        msg = Message(self.topic,
                      recipients=self.recipients,
                      html=self.content,
                      reply_to=self.reply_email)
        mail.send(msg)
