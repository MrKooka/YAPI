from wtforms import Form, BooleanField, StringField, validators,IntegerField,SubmitField
from wtforms.validators import DataRequired,NumberRange,ValidationError
from flask_wtf import FlaskForm
import re

def youtube_url_validation(form,field):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, field.data)
    if not youtube_regex_match:
        raise ValidationError('Ввидите ссылку на Youtube видео')
class Search_form(FlaskForm):
	url = StringField('Ссылка на видео',validators=[DataRequired(),youtube_url_validation])
	maxResults = IntegerField('Количество комментариев',
							   validators=[DataRequired(),
							   NumberRange(min=0,max=100000,
							   message='В поле "колличество комментариев" принимаются только целые числа')])
	submit = SubmitField("Найти")