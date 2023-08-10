from flask import Blueprint, render_template
from clothes.posts.forms import SearchForm


errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
	return render_template('errors/404.html',form1 = SearchForm()), 404

@errors.app_errorhandler(403)
def error_403(error):
	return render_template('errors/403.html',form1 = SearchForm()), 403

@errors.app_errorhandler(500)
def error_500(error):
	return render_template('errors/500.html',form1 = SearchForm()), 500