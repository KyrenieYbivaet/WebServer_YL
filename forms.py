from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
							   Length, EqualTo)

from models import User

def name_exists(form, field):
	if User.select().where(User.username == field.data).exists():
		raise ValidationError('Имя пользователя занято.')

def email_exists(form,field):
	if User.select().where(User.email == field.data).exists():
		raise ValidationError('Почта уже была использована.')

class RegisterForm(Form):
	username = StringField(
		'Имя пользователя',
		validators=[
			DataRequired(),
			Regexp(
				r'^[a-zA-Z0-9_]+$',
				message = ('Имя пользователя должно состоять из одного слова, разрешено использовать буквы, числа и нижние подчеркивания.')
				),
			name_exists
		])

	email = StringField(
		'Почта',
		validators=[
			DataRequired(),
			Email(),
			email_exists
		])

	password = PasswordField(
		'Пароль',
		validators=[
			DataRequired(),
			Length(min=2),
			EqualTo('password2', message = 'Пароли должны совпадать!')
		])
	password2 = PasswordField(
		'Подтвердите П@$$w0rd',
		validators=[DataRequired()
		])


class LoginForm(Form):
	email = StringField('Почти', validators=[DataRequired(), Email()])
	password = PasswordField('Пароль', validators=[DataRequired()])

class PostForm(Form):
	content = TextAreaField("Что у Вас нового?", validators = [DataRequired()])
