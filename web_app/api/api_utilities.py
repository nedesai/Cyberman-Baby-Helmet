NO_ERRORS = "NO_ERRORS"

#-----------#
# Utilities #
#-----------#
def data_missing_keys(json_data, required_keys):
    missing_keys = False
    for key in required_keys:
        if key not in json_data:
            print(key)
            missing_keys = True
    return missing_keys

def check_user_permissions(db, username, patient):
    error = NO_ERRORS
    cur = db.cursor()
    cur.execute('SELECT * FROM Patient WHERE username=\'' + username + '\'')
    if len(cur.fetchall()) == 0:
        error = 'Error: User does not have permission to access this patient\'s models'
    return error, 403