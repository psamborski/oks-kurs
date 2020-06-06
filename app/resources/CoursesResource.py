from app import db
import datetime


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    organizingMeetingDate = db.Column(db.Date, nullable=False)
    organizingMeetingTime = db.Column(db.Time, nullable=False)
    startDate = db.Column(db.Date(), nullable=False)
    startTime = db.Column(db.Time, nullable=False)
    studentLimit = db.Column(db.Integer, nullable=True)
    cost = db.Column(db.Integer, nullable=False, default=1400)
    additionalData = db.Column(db.String(120), nullable=True)
    students = db.relationship('Students', backref='course', lazy=True)

    def __repr__(self):
        return f"Course('{self.name}, '{self.startDate}', '{self.cost}')"


def get_current_course():
    """
    Get closest course.
    :return: Course data or None.
    """
    current_date = datetime.datetime.now().date()
    current_course = Courses.query. \
        filter(Courses.startDate >= current_date). \
        order_by(Courses.startDate.asc()). \
        first()

    return current_course


def get_four_future_courses():
    """
    Get three planned courses.
    :return: Courses data.
    """

    current_date = datetime.datetime.now().date()
    courses = Courses.query. \
        filter(Courses.startDate >= current_date). \
        order_by(Courses.startDate.asc()). \
        limit(4).\
        all()

    return courses


def get_course_by_id(course_id):
    """
    Get course by ID.
    :return: Course data or None.
    """
    course = Courses.query. \
        filter_by(id=course_id). \
        first_or_404()

    return course


def get_all_courses(page):
    """
    Get all courses.
    :return: Courses data.
    """

    courses = Courses.query \
        .order_by(Courses.startDate.desc()) \
        .paginate(page=page, per_page=6)

    return courses
