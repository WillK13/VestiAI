from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, RadioField, ValidationError
from wtforms.validators import DataRequired, NumberRange

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	def validate_content(form, field):
		if 'fuck' in field.data.lower():
			raise ValidationError('Please avoid profane language')
		if 'kike' in field.data.lower():
			raise ValidationError('Please avoid profane language')
		if 'ass' in field.data.lower():
			raise ValidationError('Please avoid profane language')
		if 'bitch' in field.data.lower():
			raise ValidationError('Please avoid profane language')
		if 'dick' in field.data.lower():
			raise ValidationError('Please avoid profane language')
		if 'pussy' in field.data.lower():
			raise ValidationError('Please avoid profane language')
		if 'motherfucker' in field.data.lower():
			raise ValidationError('Please avoid profane language')
		if 'retard' in field.data.lower():
			raise ValidationError('Please avoid profane language')
	submit = SubmitField('Post')

class SearchForm(FlaskForm):
	searched = StringField('Searched', validators=[DataRequired()])
	submit = SubmitField('Post')

class ClothesForm(FlaskForm):
	formality = IntegerField('Pick a number 1-10 on how formal you want your outfit.', validators=[DataRequired(), NumberRange(min=0, max=10)])
	mood = IntegerField('Pick a number 1-10 to best describe your mood (10 being the best).', validators=[DataRequired(), NumberRange(min=0, max=10)])
	temperature = RadioField('Please pick the closest answer for where you will be wearing this outfit.', validators=[DataRequired()], choices=['Cold', 'Cool', 'Room temp', 'Warm', 'Hot'])
	additional = StringField('Any additional comments for our AI. This helps us generate more accurate outfits.')
	submit = SubmitField('Get Outfit')