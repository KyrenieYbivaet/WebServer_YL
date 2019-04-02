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
		'Username',
		validators=[
			DataRequired(),
			Regexp(
				r'^[a-zA-Z0-9_]+$',
				message = ('Имя пользователя должно состоять из одного слова, разрешено использовать буквы, числа и нижние подчеркивания.')
				),
			name_exists
		])

	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email(),
			email_exists
		])

	password = PasswordField(
		'Password',
		validators=[
			DataRequired(),
			Length(min=2),
			EqualTo('password2', message = 'Пароли должны совпадать!')
		])
	password2 = PasswordField(
		'Подтвердите пароль',
		validators=[DataRequired()
		])


class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])

class PostForm(Form):
	content = TextAreaField("Что у Вас нового?", validators = [DataRequired()])