from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_user, current_user, logout_user, login_required
# from flask_weasyprint import HTML, render_pdf  # required packages installed on server
import pdfkit

from app import db, bcrypt
from app.forms.courseForm import CourseForm
# database
from app.forms.loginForm import LoginForm
from app.forms.userForm import UserForm
from app.models.functions import reformat_date, reformat_course
from app.resources.StudentsResource import get_students_by_course, delete_students_by_course
from app.resources.CoursesResource import Courses, get_course_by_id, get_current_course, get_all_courses
from app.resources.UsersResource import get_user

CMS = Blueprint('CMS', __name__)


@CMS.route('/admin')
@login_required
def index():
    closest_course = get_current_course()

    if closest_course is None:
        closest_course_id = None
    else:
        closest_course_id = closest_course.id

    return render_template('cms/index.html', closest_course_id=closest_course_id)


@CMS.route('/admin/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('CMS.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(username=form.login.data)
        if user and bcrypt.check_password_hash(user.passwordHash, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('CMS.index'))
        else:
            flash('Wprowadzono niepoprawny login lub hasło.', 'error')

    return render_template('cms/login.html', form=form)


@CMS.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('CMS.login'))


@CMS.route('/admin/ustawienia', methods=['POST', 'GET'])
@login_required
def settings():
    form = UserForm()
    user = get_user(current_user.username)

    if request.method == 'POST' and form.validate_on_submit():
        user.email = form.email.data
        db.session.commit()

        flash(f'Zaktualizowano adres e-mail.', 'success')

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Niepoprawny adres e-mail.', 'warning')

    elif request.method == 'GET':
        form.email.data = user.email

    return render_template('cms/settings.html', form=form, user=user)


@CMS.route('/admin/kursy')
@login_required
def all_courses():
    page = request.args.get('strona', 1, type=int)

    courses = get_all_courses(page)
    for course in courses.items:
        reformat_date(course.startDate)

    return render_template('cms/all-courses.html', courses=courses)


@CMS.route('/admin/kursy/dodaj', methods=['POST', 'GET'])
@login_required
def add_course():
    form = CourseForm()
    if request.method == 'POST' and form.validate_on_submit():
        course = Courses(
            name=form.name.data,
            organizingMeetingDate=form.organizing_meeting_date.data,
            organizingMeetingTime=form.organizing_meeting_time.data,
            startDate=form.start_date.data,
            startTime=form.start_time.data,
            cost=form.cost.data,
            studentLimit=form.limit.data,
            additionalData=form.additionalData.data
        )

        db.session.add(course)
        db.session.commit()

        flash('Utworzono nowy kurs.', 'success')

        return redirect(url_for('CMS.all_courses'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/course-form.html', form=form, action='add')

    return render_template('cms/course-form.html', form=form, action='add')


@CMS.route('/admin/kursy/<int:course_id>/edytuj', methods=['POST', 'GET'])
@login_required
def update_course(course_id):
    course = get_course_by_id(course_id)

    form = CourseForm()

    if request.method == 'POST' and form.validate_on_submit():
        course.name = form.name.data
        course.startDate = form.start_date.data
        course.startTime = form.start_time.data
        course.organizingMeetingDate = form.organizing_meeting_date.data
        course.organizingMeetingTime = form.organizing_meeting_time.data
        course.studentLimit = form.limit.data
        course.cost = form.cost.data
        course.additionalData = form.additionalData.data

        db.session.commit()

        flash('Zaktualizowano kurs.', 'success')

        return redirect(url_for('CMS.specific_course', course_id=course_id))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/course-form.html', form=form, action='edit')

    elif request.method == 'GET':
        form.name.data = course.name
        form.start_date.data = course.startDate
        form.start_time.data = course.startTime
        form.organizing_meeting_date.data = course.organizingMeetingDate
        form.organizing_meeting_time.data = course.organizingMeetingTime
        form.limit.data = course.studentLimit
        form.cost.data = course.cost
        form.additionalData.data = course.additionalData

        return render_template('cms/course-form.html', form=form, action='edit')

    return render_template('cms/course-form.html', form=form, action='edit')


@CMS.route("/admin/kursy/<int:course_id>/usun", methods=['POST'])
@login_required
def delete_course(course_id):
    course = get_course_by_id(course_id)

    delete_students_by_course(course_id)
    db.session.delete(course)
    db.session.commit()

    # deleting multiple rows can be quicker with engine
    # https://stackoverflow.com/questions/39773560/sqlalchemy-how-do-you-delete-multiple-rows-without-querying
    # https: // docs.sqlalchemy.org / en / latest / core / connections.html

    flash('Kurs został usunięty.', 'success')
    return redirect(url_for('CMS.all_courses'))


@CMS.route('/admin/kursy/id_<int:course_id>', methods=['POST', 'GET'])
@login_required
def specific_course(course_id):
    page = request.args.get('strona', 1, type=int)

    course = get_course_by_id(course_id)
    formatted_course = reformat_course(get_course_by_id(course_id))

    students = get_students_by_course(course_id, page)

    return render_template('cms/course.html',
                           course=course,
                           formatted_course_data=formatted_course,
                           students=students
                           )


@CMS.route('/admin/kursy/id_<int:course_id>/<string:course_namestring>.pdf', methods=['GET'])
@login_required
def course_to_pdf(course_id, course_namestring):
    # course namstring: kurs_dd-mm-YYYY.pdf

    course = get_course_by_id(course_id)
    formatted_course = reformat_course(get_course_by_id(course_id))

    students = get_students_by_course(course_id)
    students_len = len(students)

    html = render_template('cms/course-pdf.html',
                           course=course,
                           formatted_course=formatted_course,
                           students=students,
                           students_counter=students_len,
                           url=request.url_root[:-1]
                           )

    pdf = pdfkit.from_string(html, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'filename=' + course_namestring + '.pdf'

    return response
    # return render_pdf(HTML(string=html))
    # return render_template('cms/course-pdf.html',
    #                        course=course,
    #                        formatted_course=formatted_course,
    #                        students=students,
    #                        students_counter=students_len
    #                        )

# TODO: płatność
