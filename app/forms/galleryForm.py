from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import BooleanField, MultipleFileField
from wtforms.validators import DataRequired, Optional


class GalleryForm(FlaskForm):
    photos = MultipleFileField(label='Dodaj zdjęcia',
                               validators=[
                                   DataRequired(message='Nie wybrano żadnych zdjęć.'),
                                   FileAllowed(['jpg', 'png'],
                                               message="Nieprawidłowy format pliku(ów) (dozwolone: jpg, png).")
                               ])
    scale = BooleanField(label='Dopasuj zdjęcia do wymiarów galerii',
                         validators=[
                             Optional()
                         ])
