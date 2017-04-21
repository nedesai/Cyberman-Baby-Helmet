from flask import *
from extensions import connect_to_database

photos = Blueprint('photos', __name__, template_folder='templates')

@photos.route('/api/v1/photos', methods=['GET'])
def photos_route():
    if 'username' not in session:
        return jsonify(errors="User not logged in")
    username = session['username']

    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM PhotoZip WHERE username=\'{}\''.format(username))
    results = cur.fetchall()

    # Only one result should be returned since users can only have one zipfile
    # of photos hosted on our site at a time
    #if(len(results) > 1):
     #   return jsonify(errors="Too many files")

    # Return the URL for the zipfile if one exists and a notification
    # that it does not exist otherwise metadata
    if (len(results) >= 1):
        # Remove this zipfile's metadata from database
        cur.execute('DELETE FROM PhotoZip WHERE username=\'{}\''.format(username))
        photos_url = results[0]['url']
        return jsonify(status="ZIPFILE_FOUND", url=photos_url)
    else:
        return jsonify(status="NO_ZIPFILE_FOUND")
