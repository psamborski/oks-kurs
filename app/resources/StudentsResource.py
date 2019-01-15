from app import db


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=True)
    age = db.Column(db.String(4), nullable=True)
    courseId = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    def __repr__(self):
        return f"Student('{self.name}', '{self.surname}', '{self.phone}', '{self.email}')"


def get_students_by_course(course_id, page=None):
    """
    Get students by course.
    :return: Students data or None.
    """
    if page is None:
        students = Students.query.filter_by(courseId=course_id) \
            .order_by(Students.id.desc()) \
            .all()
    else:
        students = Students.query.filter_by(courseId=course_id) \
            .order_by(Students.id.desc()) \
            .paginate(page=page, per_page=10)  # not just 'id' because it shadows built-in function

    return students


def delete_students_by_course(course_id):
    """
    Deletes certain course students.
    :param course_id:
    :return:
    """
    db.session.query(Students).filter(Students.courseId == course_id).delete()
