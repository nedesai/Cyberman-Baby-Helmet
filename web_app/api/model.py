from flask import *
from extensions import connect_to_database
from datetime import datetime
from .api_utilities import data_missing_keys, check_user_permissions, NO_ERRORS
import boto3
import hashlib
import os
import fbx

model = Blueprint('model', __name__, template_folder='templates')

#-----------#
# Model API #
#-----------#
def obj2fbx(objpath, fbxpath):
    '''
    take input filename and convert to fbx file
    from http://stackoverflow.com/questions/34132474/convert-obj-to-fbx-with-python-fbx-sdk
    '''
    # Create an SDK manager

    manager = fbx.FbxManager.Create()

    # Create a scene
    scene = fbx.FbxScene.Create(manager, "")

    # Create an importer object
    importer = fbx.FbxImporter.Create(manager, "")


    # Specify the path and name of the file to be imported
    importstat = importer.Initialize(objpath, -1)

    importstat = importer.Import(scene)
    # Create an exporter object

    exporter = fbx.FbxExporter.Create(manager, "")

    # Specify the path and name of the file to be imported
    exportstat = exporter.Initialize(fbxpath, -1)
    exportstat = exporter.Export(scene)

    return 0

def uploads3(file, filename):
    '''
    this function upload file to aws S3 storage and 
    return the url of that file on S3 that can be accessed
    '''

    #connect to aws s3 with the key configured in the system file
    s3_client = boto3.client('s3')
    #upload the file to s3 storage with filename as its name.
    #the bucket babyhead is configured to be public for now
    s3_client.upload_file(file, 'babyhead', filename)
    url = 'https://s3.amazonaws.com/babyhead/' + filename
    return url

def processobj(file, filename):
    '''
    when the user upload a obj file to the server,
    this function create temp file for this obj, convert it to fbx,
    then upload both obj and fbx to S3, return their urls and 
    delete the temp file.
    '''
    objpath = '/home/ubuntu/tempmodel/' + filename + '.obj'
    fbxpath = '/home/ubuntu/tempmodel/' + filename + '.fbx'
    # save the file from request.files['file'] locally
    file.save(objpath)
    #convert obj to fbx and save it at fbxpath
    obj2fbx(objpath, fbxpath)
    #upload both obj and fbx
    obj_url = uploads3(objpath,filename + '.obj')
    fbx_url = uploads3(fbxpath,filename + '.fbx')
    os.remove(objpath)
    os.remove(fbxpath)
    return obj_url, fbx_url



@model.route('/api/v1/model', methods=['GET', 'POST', 'DELETE'])
def model_route():
    db = connect_to_database()

    #---------------------------------------------#
    # Error-checking for DELETE and POST requests #
    #---------------------------------------------#
    if request.method == 'DELETE' or request.method == 'POST':
        json_data = request.get_json()

        # Check for missing keys
        required_keys = ['username', 'patientid']
        if request.method == 'DELETE':
            required_keys.append('modelid')
        elif request.method == 'POST':
            required_keys.append('filetype, description')
        if data_missing_keys(json_data, required_keys):
            error = 'Error: request missing required keys'
            return jsonify(error=error), 422

        # Check if the user has permission to access this patient's data
        error, status_code = check_user_permissions(db, json_data['username'], json_data['patientid'])
        if error != NO_ERRORS:
            return jsonify(error=error), status_code

    #--------------#
    # GET requests #
    #--------------#
    if request.method == 'GET':
        username = request.args.get('username')
        patientid = request.args.get('patientid')

        #----------------#
        # Error-checking #
        #----------------#
        # Check for missing query parameters
        if username == None or patientid == None:
            error = 'Error: request missing required query parameters'
            return jsonify(error=error), 422

        # Check if the user has permission to access this patient's data
        error, status_code = check_user_permissions(db, username, patientid)
        if error != NO_ERRORS:
            return jsonify(error=error), status_code

        #-----------------------#
        # Get model information #
        #-----------------------#
        cur = db.cursor()
        cur.execute('SELECT url, fbx_url, filename, description, lastmodified FROM Model WHERE patientid=' + patientid)
        models = []
        for m in cur.fetchall():
            models.append( { 'url': m['url'], 'fbx_url': m['fbx_url'], 'filename': m['filename'], 'description': m['description'], 'lastmodified': m['lastmodified'] } )

        return jsonify(models=models), 200

    #---------------#
    # POST requests #
    #---------------#
    elif request.method == "POST":
        json_data = request.get_json()
        model_description = json_data['description']
        username = json_data['username']
        patientid = json_data['patientid']
        model_file = request.files['file']
        current_date_time = datetime.now()

        #hash_url = hashlib.sha512(str.encode(patientid + str(current_date_time)))

        filename, filetype = os.path.splitext(model_file.filename)

        urls = processobj(model_file, filename)
        #s3_client = boto3.client('s3')
        #s3_client.upload_file(model_file, 'babyhead', model_file)
        # s3_client.upload_file(model_file, 'babyhead', '<name-of-the-file>')
        #url = 'https://s3.amazonaws.com/babyhead/' + filename
        
        cur = db.cursor()
        sql_string = "INSERT INTO Model (patientid, filetype, url, fbx_url, description, filename) VALUES ('"
        sql_string += patientid + "', '" + filetype + "', '"
        sql_string += urls[0] + "', '" + urls[1] + "', '" + model_description + "', '" + filename + "');"
        cur.execute(sql_string)

        return jsonify({}), 200

    #-----------------#
    # DELETE requests #
    #-----------------#
    elif request.method == 'DELETE':
        json_data = request.get_json()
        cur = db.cursor()
        cur.execute('DELETE FROM Model WHERE modelid=' + json_data['modelid'])
        return jsonify({}), 200

