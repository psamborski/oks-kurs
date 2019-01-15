import datetime

from app.resources.CoursesResource import Courses, get_course_by_id, get_three_future_courses
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
                        'studentCount': len(get_students_by_course(course.id))
                    }
                )

    return reformatted_data


def prepare_courses_for_radio():
    """
    Prepare courses data for sign up form.

    :return: Courses list.
    """

    three_closest_courses = get_three_future_courses()
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
