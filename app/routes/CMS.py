from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_user, current_user, logout_user, login_required
# from flask_weasyprint import HTML, render_pdf  # required packages installed on server
import pdfkit

from app import db, bcrypt
from app.forms.courseForm import CourseForm
from app.forms.galleryAddForm import GalleryAddForm
from app.forms.galleryUpdateForm import GalleryUpdateForm
from app.forms.loginForm import LoginForm
from app.forms.popUpForm import PopUpForm
from app.forms.pricesForm import PricesForm
from app.forms.userForm import UserForm

from app.models.MailModel import Mail
from app.models.functions import reformat_date, reformat_course, save_picture, get_photo_title, scale_photo, \
    delete_photo

from app.resources.GalleryResource import get_all_photos, Gallery, get_photo_by_id
from app.resources.PopUpResource import get_pop_up
from app.resources.PricesResource import get_all_prices
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
        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - OSK Kurs', 'Błąd przy zmienie e-maila: ' + str(e),
                        'psambek@gmail.com')
            mail.send()

            return render_template('cms/settings.html', form=form, user=user)

        flash(f'Zaktualizowano adres e-mail.', 'success')

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Niepoprawny adres e-mail.', 'warning')

    elif request.method == 'GET':
        form.email.data = user.email

    return render_template('cms/settings.html', form=form, user=user)


@CMS.route('/admin/cennik', methods=['POST', 'GET'])
@login_required
def prices():
    form = PricesForm()
    all_prices = get_all_prices()

    if request.method == 'POST' and form.validate_on_submit():
        # user.email = form.email.data
        for price in all_prices:
            # get value for specific price
            value = getattr(form, price.name)
            price.price = value.data

        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - OSK Kurs', 'Błąd przy zmienie cennika: ' + str(e),
                        'psambek@gmail.com')
            mail.send()

            return render_template('cms/prices.html', form=form)

        flash(f'Zaktualizowano cennik.', 'success')

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Cennik nie został uzupełniony poprawnie.', 'warning')

    elif request.method == 'GET':
        for price in all_prices:
            current_input = getattr(form, price.name)
            current_input.data = price.price
            setattr(form, price.name, current_input)

    return render_template('cms/prices.html', form=form)


@CMS.route('/admin/popup', methods=['POST', 'GET'])
@login_required
def popup():
    form = PopUpForm()
    pop_up = get_pop_up()

    if request.method == 'POST' and form.validate_on_submit():
        pop_up.header = form.header.data
        pop_up.body = form.body.data
        pop_up.photo = form.photo.data
        pop_up.show = 1 if form.show.data else 0

        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - OSK Kurs', 'Błąd przy zmienie pop upa: ' + str(e),
                        'psambek@gmail.com')
            mail.send()

            return render_template('cms/popup.html', form=form)

        flash(f'Zaktualizowano pop up.', 'success')

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Pop up nie został uzupełniony poprawnie.', 'warning')

    elif request.method == 'GET':
        form.header.data = pop_up.header
        form.body.data = pop_up.body
        form.photo.data = pop_up.photo
        form.show.data = pop_up.show

    return render_template('cms/popup.html', form=form)


@CMS.route('/admin/galeria', methods=['POST', 'GET'])
@login_required
def gallery():
    # get add photos form
    add_form = GalleryAddForm()

    # get update form
    current_gallery = get_all_photos()

    current_photos = []

    # get current gallery and reformat it
    for photo in current_gallery:
        current_photos.append(
            {
                "title": photo.title,
                "order": photo.order,
                "src": photo.src,
                "photo_id": photo.id
            }
        )

    update_form = GalleryUpdateForm(photos=current_photos)
    # finish getting

    if request.method == 'POST':
        # ADD PHOTOS form
        if request.form["type"] == 'add' and add_form.validate_on_submit():
            # if form is ok
            form_photos = request.files.getlist(add_form.photos.name)

            if form_photos:
                # double check if there are any photos

                for photo in form_photos:
                    filename = photo.filename
                    picture_name = get_photo_title(photo)

                    if add_form.scale.data:
                        # if scaling option is checked, scale
                        photo = scale_photo(photo)

                    save_picture(photo, picture_name)

                    photo_to_gallery = Gallery(
                        title=filename,
                        src=picture_name
                    )

                    db.session.add(photo_to_gallery)

                try:
                    db.session.commit()
                    flash('Zaktualizowano galerię.', 'success')

                    # the only way to deal with strange error in creating empty update form after add request
                    # it also makes refresh not triggering window with asking for uploading form again
                    return redirect(url_for('CMS.gallery'))

                except Exception as e:
                    flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
                    mail = Mail('Błąd - OSK Kurs', 'Błąd przy aktualizacji galerii: ' + str(e),
                                'psambek@gmail.com')

                    mail.send()

                    return render_template('cms/photos.html',
                                           add_form=add_form,
                                           update_form=update_form,
                                           photos=current_gallery
                                           )

            else:
                # if there's not any photo
                flash('Wczytane pliki mają niepoprawny format lub nie wybrano żadnych zdjęć.', 'warning')

                # the only way to deal with strange error in creating empty update form after add request
                # it also makes refresh not triggering window with asking for uploading form again
                return redirect(url_for('CMS.gallery'))

        elif request.form["type"] == 'add' and not add_form.validate_on_submit():
            # if add form doesn't validate
            flash('Wczytane pliki mają niepoprawny format lub nie wybrano żadnych zdjęć.', 'warning')

        # UPDATE PHOTOS form
        if request.form["type"] == 'update' and update_form.validate_on_submit():
            try:

                for gallery_object, form_photo in zip(current_gallery, update_form.photos):
                    gallery_object.title = form_photo.title.data
                    gallery_object.order = form_photo.order.data

                db.session.commit()

            except Exception as e:
                flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
                mail = Mail('Błąd - OSK Kurs', 'Błąd przy aktualizacji galerii: ' + str(e),
                            'psambek@gmail.com')

                mail.send()

                return render_template('cms/photos.html',
                                       add_form=add_form,
                                       update_form=update_form,
                                       photos=current_gallery
                                       )

            flash('Zaktualizowano galerię.', 'success')

        elif request.form["type"] == 'update' and not update_form.validate_on_submit():
            # if update form doesn't validate
            flash('Wprowadzone dane są niepoprawne.', 'warning')

    return render_template('cms/photos.html',
                           add_form=add_form,
                           update_form=update_form,
                           photos=current_gallery
                           )


@CMS.route("/admin/galeria/<int:photo_id>/usun", methods=['POST'])
@login_required
def delete_photo_from_gallery(photo_id):
    photo = get_photo_by_id(photo_id)

    try:
        db.session.delete(photo)
        db.session.commit()

        delete_photo(photo.src)
    except Exception as e:
        flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
        mail = Mail('Błąd - OSK Kurs', 'Błąd przy usuwaniu kursu: ' + str(e),
                    'psambek@gmail.com')
        mail.send()

        return redirect(url_for('CMS.gallery'))

    # deleting multiple rows can be quicker with engine
    # https://stackoverflow.com/questions/39773560/sqlalchemy-how-do-you-delete-multiple-rows-without-querying
    # https: // docs.sqlalchemy.org / en / latest / core / connections.html

    flash('Zdjęcie zostało usunięte.', 'success')
    return redirect(url_for('CMS.gallery'))


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
        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - OSK Kurs', 'Błąd przy tworzeniu kursu: ' + str(e),
                        'psambek@gmail.com')
            mail.send()

            return render_template('cms/course-form.html', form=form, action='add')

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

        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - OSK Kurs', 'Błąd przy edycji kursu: ' + str(e),
                        'psambek@gmail.com')
            mail.send()

            return render_template('cms/course-form.html', form=form, action='edit')

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

    try:
        db.session.delete(course)
        db.session.commit()
    except Exception as e:
        flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
        mail = Mail('Błąd - OSK Kurs', 'Błąd przy usuwaniu kursu: ' + str(e),
                    'psambek@gmail.com')
        mail.send()

        return redirect(url_for('CMS.all_courses'))

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
                           url=request.url_root[:-1]  # url needed to build style file link (without "/" at the end)
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
