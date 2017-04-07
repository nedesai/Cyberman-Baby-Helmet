from flask import *

import unicodedata
import hashlib
import re
import uuid

main = Blueprint('main', __name__, static_url_path='static',template_folder='templates')


@main.route('/', methods=['GET'])
def main_route():
	if 'username' not in session:
		return redirect(url_for('main.signin'))
	else:
		return render_template("index.html")

@main.route('/login', methods=['GET'])
def signin():
	if 'username' in session:
		return render_template("index.html")
	else:
		return render_template("signin.html")
