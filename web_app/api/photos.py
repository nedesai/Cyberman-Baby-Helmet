from flask import *
from extensions import connect_to_database

photos = Blueprint('photos', __name__, template_folder='templates')

@photos.route('/api/v1/photos', methods=['GET'])
def photos_route():
    username = request.args.get('username')

    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM PhotoZip WHERE username=\'{}\''.format(username))
    results = cur.fetchall()

    # Only one result should be returned since users can only have one zipfile
    # of photos hosted on our site at a time
    assert(len(results) <= 1)

    # Return the URL for the zipfile if one exists and a notification
    # that it does not exist otherwise
    if len(results == 1):
        photos_url = results[0]['url']
        return jsonify(status="ZIPFILE_FOUND", url=photos_url)
    else:
        return jsonify(status="NO_ZIPFILE_FOUND")