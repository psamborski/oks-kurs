from app import db


class PopUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(240), nullable=False)
    body = db.Column(db.String(1024), nullable=False)
    photo = db.Column(db.String(480), nullable=True)
    show = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"PopUp('{self.header}')"


def get_pop_up():
    """
    Get the only pop up record.
    :return: Pop up data data or None.
    """
    pop_up = PopUp.query. \
        first_or_404()

    return pop_up
