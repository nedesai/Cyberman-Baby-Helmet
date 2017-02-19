from flask import *

import unicodedata
import hashlib
import re
import uuid

main = Blueprint('main', __name__, static_url_path='static',template_folder='templates')


@main.route('/', methods=['GET'])
def main_route():
	return render_template("index.html")