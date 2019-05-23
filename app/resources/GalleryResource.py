from app import db


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False)
    src = db.Column(db.String(240), nullable=False)
    order = db.Column(db.Integer, nullable=True, default=1)

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


def get_photo_by_id(photo_id):
    """
    Get photo by ID.
    :return: Photo data or None.
    """
    photo = Gallery.query. \
        filter_by(id=photo_id). \
        first_or_404()

    return photo

