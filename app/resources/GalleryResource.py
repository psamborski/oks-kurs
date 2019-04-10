from app import db


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    src = db.Column(db.String(240), nullable=False)
    order = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return f"Gallery('{self.title}, '{self.src}', '{self.order}')"


def get_all_photos():
    """
    Get all Gallery.
    :return: Gallery data.
    """

    photos = Gallery.query \
        .order_by(Gallery.order.asc())\
        .all()
    return photos
