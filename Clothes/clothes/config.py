import os

class Config:
	SECRET_KEY='abb95975655ac0ba2801e9e4061663a8'
	SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
	EMAIL_USER='will@kaminskis.org'
	MAIL_PASS='Zoewillie75'
	#SECRET_KEY = os.environ.get('SECRET_KEY')
	#SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	#MAIL_USERNAME = os.environ.get('EMAIL_USER')
	#MAIL_PASSWORD = os.environ.get('EMAIL_PASS')