from app import db


class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Price('{self.name}, '{self.price}')"


def get_price_by_id(course_id):
    """
    Get course by ID.
    :return: Course data or None.
    """
    course = Prices.query. \
        filter_by(id=course_id). \
        first_or_404()

    return course


def get_all_prices():
    """
    Get all prices.
    :return: prices data.
    """

    prices = Prices.query.all()
    return prices
