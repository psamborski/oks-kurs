import datetime
import os
import secrets
import cv2
import numpy
from PIL import Image
from werkzeug.utils import secure_filename

from app import app
from app.resources.CoursesResource import Courses, get_course_by_id, get_four_future_courses
from app.resources.StudentsResource import Students  # it makes CoursesResource work (db relationship)
from app.resources.StudentsResource import get_students_by_course


def reformat_date(course_date):
    """
    Reformats dates.
    :param course_date:
    :return:
    """
    date = datetime.datetime.strptime(str(course_date), '%Y-%m-%d').strftime('%d.%m.%Y')

    return date


def reformat_time(course_time):
    """
    Reformats time value.
    :param course_time:
    :return:
    """
    time = course_time.strftime('%H:%M')

    # isoformat(timespec='minutes')  timespec = 'minutes' above python 3.5

    return time


def reformat_course(courses):
    """
    Return dict with nicely represented dates and hours.
    :param courses:
    :return:
    """

    if isinstance(courses, Courses):  # if it's just one course object
        reformatted_data = {
            'startDate': reformat_date(courses.startDate),
            'organizingMeetingDate': reformat_date(courses.organizingMeetingDate),
            'startTime': reformat_time(courses.startTime),
            'organizingMeetingTime': reformat_time(courses.organizingMeetingTime)
        }
    else:
        reformatted_data = []
        for course in courses:
            if isinstance(course, Courses):
                reformatted_data.append(
                    {
                        'startDate': reformat_date(course.startDate),
                        'organizingMeetingDate': reformat_date(course.organizingMeetingDate),
                        'startTime': reformat_time(course.startTime),
                        'organizingMeetingTime': reformat_time(course.organizingMeetingTime),
                        'studentLimit': course.studentLimit,
                        'studentCount': len(get_students_by_course(course.id)),
                        'additionalData': course.additionalData
                    }
                )

    return reformatted_data


def prepare_courses_for_radio():
    """
    Prepare courses data for sign up form.

    :return: Courses list.
    """

    three_closest_courses = get_four_future_courses()
    radio_courses = []

    for course in three_closest_courses:
        radio_courses.append(
            (int(course.id), str(reformat_date(course.startDate) + '&nbsp;r.'))
        )
    return radio_courses


def validate_student_limit(course_id):
    """
    Check if it's possible to register for the course looking at students limit.
    :param course_id:
    :return: False or True
    """
    course = get_course_by_id(course_id)
    student_count = len(get_students_by_course(course_id))

    if course.studentLimit != 0 and student_count >= course.studentLimit:
        return False
    else:
        return True


def reformat_prices(all_prices):
    reformatted_prices = {}
    for price in all_prices:
        reformatted_prices[price.name] = price.price

    return reformatted_prices


def save_picture(picture, picture_name):
    picture_path = os.path.join(app.root_path, 'static/images/gallery', picture_name)
    picture.save(picture_path)

    return True


def get_photo_title(picture):
    random_hex = secrets.token_hex(6)
    f_name, f_ext = os.path.splitext(picture.filename)
    picture_fn = secure_filename(f_name)[:10] + "_" + random_hex + f_ext
    return picture_fn


def scale_photo(picture):
    # resize photo for back and foreground
    pil_picture = Image.open(picture)
    width, height = pil_picture.size

    # scale back properly // pil_background.thumbnail(size, Image.ANTIALIAS) - problem with small pictures
    if width / height > 1.685:  # 1164/689
        bratio = 698/height
        fratio = 1154/width
        back_size = int(width*bratio), 689
        for_size = 1154, int(height*fratio)
    else:
        bratio = 1154/width
        fratio = 689/height
        back_size = 1154, int(height*bratio)
        for_size = int(width*fratio), 689
    pil_background = pil_picture.resize(back_size, Image.ANTIALIAS)
    pil_foreground = pil_picture.resize(for_size, Image.ANTIALIAS)

    # crop back properly
    back_width, back_height = pil_background.size
    if width / height > 1.685:
        difference = back_width - 1154  # get difference between target size and current size
        pil_background = pil_background.crop((int(difference/2), 0, int(back_width-difference/2), back_height))
    else:
        difference = back_height - 689  # get difference between target size and current size
        pil_background = pil_background.crop((0, int(difference/2), back_width, int(back_height-difference/2)))

    # cropped = img.crop((x, y, x + width, y + height))
    # x and y are the top left coordinate on image
    # x + width and y + height are the width and height respectively of the region that you want to crop starting at x and ypoint
    # Note: x + width and y + height are the bottom right coordinate of the cropped region.

    # convert to proper color model
    pil_background = pil_background.convert('RGB')
    pil_foreground = pil_foreground.convert('RGBA')

    # convert to cv2 format for blurring
    cv_background = numpy.array(pil_background)
    # Convert RGB to BGR
    cv_background = cv_background[:, :, ::-1].copy()

    # blur background and convert to PIL again
    cv_background = cv2.GaussianBlur(cv_background, (55, 55), 0)  # values must be odd
    cv_background = cv2.cvtColor(cv_background, cv2.COLOR_BGR2RGB)
    pil_background = Image.fromarray(cv_background)

    # merge fore and background
    final_width, final_height = pil_foreground.size
    if width / height > 1.685:
        final_difference = 689 - final_height
        pil_background.paste(pil_foreground, (0, int(final_difference/2)), pil_foreground)
    else:
        final_difference = 1154 - final_width
        pil_background.paste(pil_foreground, (int(final_difference/2), 0), pil_foreground)

    return pil_background


def delete_photo(photo_src):
    picture_path = os.path.join(app.root_path, 'static/images/gallery', photo_src)
    os.remove(picture_path)
