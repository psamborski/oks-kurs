from flask import Blueprint, request, flash, render_template, redirect, url_for

from app import db
from app.forms.contactForm import ContactForm
from app.forms.signUpForm import SignUpForm
from app.models.MailModel import Mail
from app.models.StudentModel import Student
from app.models.functions import reformat_date, reformat_course, validate_student_limit, reformat_prices
# database
from app.resources.CoursesResource import get_current_course, get_four_future_courses, get_course_by_id
from app.resources.GalleryResource import get_all_photos
from app.resources.PopUpResource import get_pop_up
from app.resources.PricesResource import get_all_prices
from app.resources.StudentsResource import Students

mainSite = Blueprint('mainSite', __name__)


@mainSite.route('/')
def index():
    pop_up = get_pop_up()
    if not pop_up.show:
        pop_up = None
    return render_template('index.html', pop_up=pop_up)


@mainSite.route('/o-nas')
def about():
    gallery = get_all_photos()

    return render_template('about.html', gallery=gallery)


@mainSite.route('/cennik')
def pricing():
    course = get_current_course()
    all_prices = reformat_prices(get_all_prices())
    if course is None:
        price = None
    else:
        price = course.cost

    return render_template('pricing.html', current_price=price, prices=all_prices)


@mainSite.route('/zapisz-sie-na-kurs', methods=['POST', 'GET'])
def sign_up():
    form = SignUpForm().update_form()
    # See update_form method in SignUpForm class for explanation

    four_closest_courses = get_four_future_courses()
    reformatted_courses = []

    if four_closest_courses:
        reformatted_courses = zip(form.courseId, reformat_course(four_closest_courses))
        # It zips all necessary course data with form radio options.
        # form.courseId - list of four radio inputs with closest courses

    if request.method == 'POST' and form.validate_on_submit():
        if not validate_student_limit(form.courseId.data):
            flash('Przepraszamy! Nie ma już miejsc na ten kurs.', 'error')

            return render_template('sign-up.html', form=form, courses=reformatted_courses)

        student_data = Student(form).handle_form()
        student = Students(**student_data)

        course_date = reformat_date(get_course_by_id(form.courseId.data).startDate)

        db.session.add(student)
        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - OSK Kurs', 'Błąd przy rejestracji na kurs ' + course_date + ': ' + str(e),
                        'psambek@gmail.com')
            mail.send()

            return render_template('sign-up.html', form=form, courses=reformatted_courses)

        confirm_topic = 'Potwierdzenie zgłoszenia'
        notification_topic = 'Zgłoszenie na kurs: ' + \
                             student_data['name'] + ' ' + \
                             student_data['surname'] + ' (kurs: ' + \
                             course_date + ')'
        confirm_mail = Mail(confirm_topic, (form, course_date), student_data['email'], mail_type='confirm')
        notification_mail = Mail(notification_topic, (form, course_date), mail_type='notification')

        confirm_mail.send()  # TODO mail validation?
        notification_mail.send()

        flash('Dziękujemy! Zapisałeś się na kurs.', 'success')

        return redirect(url_for('mainSite.sign_up'))

    elif request.method == 'POST' and not reformatted_courses:
        flash('Przepraszamy! Obecnie żaden kurs nie jest planowany.', 'warning')

        return render_template('sign-up.html', form=form, courses=reformatted_courses)

    elif request.method == 'POST' and not form.validate_on_submit():

        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('sign-up.html', form=form, courses=reformatted_courses)

    return render_template('sign-up.html', form=form, courses=reformatted_courses)


@mainSite.route('/kontakt', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        topic = "Wiadomość od " + email + ": " + form.topic.data + " | osk-kurs.pl"
        message = form.message.data
        mail = Mail(topic=topic, content=message, recipients=None, reply_email=email)
        mail.send()

        del mail

        flash('Pomyślnie wysłano wiadomość.', 'success')

        return render_template('contact.html', form=form)
    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('contact.html', form=form)
    return render_template('contact.html', form=form)
