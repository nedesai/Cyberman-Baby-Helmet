from flask import *
from extensions import connect_to_database
from datetime import datetime
from .api_utilities import data_missing_keys, check_user_permissions, NO_ERRORS
import boto3
import hashlib
import os
#only comment out for local testing
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


def fbx2obj(fbxpath, objpath):
    obj2fbx(fbxpath, objpath)
    return 0

def stl2fbx(stlpath, fbxpath):
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


def processfbx(file, patientID, filename):
    '''
    when the user upload a fbx file to the server,
    this function create temp file for this fbx, convert it to obj,
    then upload both obj and fbx to S3, return their urls and 
    delete the temp file.
    '''
    objpath = '/home/ubuntu/tempmodel/' + patientID+'_'+filename + '.obj'
    fbxpath = '/home/ubuntu/tempmodel/' + patientID+'_'+filename + '.fbx'
    file.save(fbxpath)
    fbx2obj(fbxpath, objpath)
    obj_url = uploads3(objpath, patientID+'_'+filename + '.obj')
    fbx_url = uploads3(fbxpath, patientID+'_'+filename + '.fbx')
    os.remove(fbxpath)
    return obj_url, fbx_url


def processobj(file, patientID, filename):
    '''
    when the user upload a obj file to the server,
    this function create temp file for this obj, convert it to fbx,
    then upload both obj and fbx to S3, return their urls and 
    delete the temp file.
    '''
    objpath = '/home/ubuntu/tempmodel/' + patientID +'_'+ filename + '.obj'
    fbxpath = '/home/ubuntu/tempmodel/' + patientID +'_'+ filename + '.fbx'
    # save the file from request.files['file'] locally
    file.save(objpath)
    #convert obj to fbx and save it at fbxpath
    obj2fbx(objpath, fbxpath)
    #upload both obj and fbx
    obj_url = uploads3(objpath,patientID+'_'+filename + '.obj')
    fbx_url = uploads3(fbxpath,patientID+'_'+filename + '.fbx')
    os.remove(fbxpath)
    return obj_url, fbx_url


def processstl(file, patientID, filename):

    stlpath = '/home/ubuntu/tempmodel/' + patientID +'_'+ filename + '.stl'
    fbxpath = '/home/ubuntu/tempmodel/' + patientID +'_'+ filename + '.fbx'
    file.save(stlpath)
    stl2fbx(stlpath,fbxpath)
    stl_url = uploads3(objpath,patientID+'_'+filename + '.stl')
    #fbx_url = uploads3(fbxpath,patientID+'_'+filename + '.fbx')
    fbx_url = '#' # kinda difficult to complete the conversion from stl to fbx
    os.remove(fbxpath)
    return stl_url, fbx_url


def deleteModel(filename):
    '''
    given an uploaded filename for any model, this will delete that file from our s3 server
    '''
    
    client = boto3.client('s3')
    client.delete_object(Bucket='babyhead', Key=filename)



@model.route('/api/v1/model', methods=['GET', 'POST', 'DELETE'])
def model_route():
    db = connect_to_database()

    #--------------#
    # GET requests #
    #--------------#
    if request.method == 'GET':
        username = str(request.args.get('username'))
        patientid = str(request.args.get('patientid'))

        #----------------#
        # Error-checking #
        #----------------#
        # Check for missing query parameters
        if username == None or patientid == None or username == "" or patientid == "":
            return jsonify(errors=['Request missing required query parameters']), 422

        # Check if the user has permission to access this patient's data
        cur = db.cursor()
        cur.execute("SELECT * FROM Patient WHERE username = '" + str(username) + "' and patientid = '" + str(patientid) + "';")
        if cur.rowcount == 0:
            return jsonify(errors=["User can't access this patient"]), 403

        #-----------------------#
        # Get model information #
        #-----------------------#
        cur = db.cursor()
        cur.execute("SELECT name, description, model_url, fbx_url, filename, filetype, lastmodified FROM Model WHERE patientid = '" + str(patientid) + "' order by lastmodified DESC;")
        models = []
        for m in cur.fetchall():
            models.append( { 'name': m['name'], 'description': m['description'], 'model_url': m['model_url'], 'fbx_url': m['fbx_url'], 'filename': m['filename'], 'filetype': m['filetype'], 'lastmodified': m['lastmodified'] } )

        return jsonify(models=models), 200

    #---------------#
    # POST requests #
    #---------------#
    elif request.method == "POST":
        username = str(request.form.get('username'))
        patientID = str(request.form.get('patientid'))
        name = str(request.form.get('name'))
        description = str(request.form.get('description'))

        if 'file' not in request.files:
            return jsonify(errors=["No file included"]), 404
        else:
            model_file = request.files['file']

        #hash_url = hashlib.sha512(str.encode(patientid + str(current_date_time)))

        filename, filetype = os.path.splitext(model_file.filename)
        filename, filetype = str(filename), str(filetype)
        filetype = filetype.lower()

        cur = db.cursor()
        cur.execute("Select * from Model where patientid = '" + str(patientID) + "' and filename = '" + str(filename) + "' and filetype = '" + str(filetype) + "' and name = '" + str(name) + "';")
        if(cur.rowcount > 0):
            return jsonify(errors=["This file already exists"]), 400

        if filetype == '.fbx':
            urls = processfbx(model_file, patientID, filename)
        elif filetype == '.obj':
            urls = processobj(model_file, patientID, filename)
        elif filetype == '.stl':
            urls = processstl(model_file, patientID, filename)
        else:
            err_msg = str(filetype[1:].upper() + " filetype not supported")
            return jsonify(errors=[err_msg]), 400
        #urls = ["www.google.com", "www.google.com"]

        cur = db.cursor()
        sql_string = "INSERT INTO Model (patientid, name, description, filename, filetype, model_url, fbx_url) VALUES ('"
        sql_string += patientID + "', '" + name + "', '" + description + "', '" + filename + "', '" + filetype + "', '" + str(urls[0])  + "', '" + str(urls[1]) + "');"
        cur.execute(sql_string)

        cur = db.cursor()
        find_modified = "Select lastmodified from Model where patientid = '" + str(patientID) + "' and filename = '" + str(filename) + "' and filetype = '" + str(filetype) + "';"
        cur.execute(find_modified)

        last_mod = cur.fetchone()['lastmodified']

        return jsonify({'name': name, 'description': description, 'filename': filename, 'filetype': filetype, 'model_url': urls[0], 'fbx_url': urls[1], 'lastmodified': str(last_mod)}), 200

    #-----------------#
    # DELETE requests #
    #-----------------#
    elif request.method == 'DELETE':
        json_data = request.get_json()
        cur = db.cursor()
        cur.execute('DELETE FROM Model WHERE modelid=' + json_data['modelid'])
        filename = json_data['filename']
        deleteModel(filename)
        return jsonify({}), 200

