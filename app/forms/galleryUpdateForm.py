from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, HiddenField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class GalleryUpdateEntryForm(FlaskForm):
    """Pattern for gallery update form."""
    title = StringField(label='Tytuł zdjęcia',
                        validators=[
                            DataRequired(message='Wprowadź nazwę.'),
                            Length(max=240, message='Nazwa jest za długa.')
                        ])
    order = IntegerField(label='Kolejność (1 - dom.)',
                         validators=[
                             DataRequired(message='Podaj wartość (1 - wartość domyślna).'),
                             NumberRange(message='Podana wartość nie jest poprawną liczbą', min=1)
                         ])
    src = HiddenField(label="Ścieżka do zdjęcia")
    photo_id = HiddenField(label="ID zdjęcia")


class GalleryUpdateForm(FlaskForm):
    """A form that allows create photos fields dynamically."""
    photos = FieldList(FormField(GalleryUpdateEntryForm), min_entries=0)

