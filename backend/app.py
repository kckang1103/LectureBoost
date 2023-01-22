#
# import os
#
# import boto3
# from flask import Flask, flash, request, redirect, url_for
# from flask import send_from_directory
# from werkzeug.utils import secure_filename
#
# s3 = boto3.client(
#     "s3",
#     aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
#     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
# )
#
# UPLOAD_FOLDER = './uploads'
# ALLOWED_EXTENSIONS = {'mp4', 'py', 'txt'}
#
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.add_url_rule(
#     "/uploads/<name>", endpoint="download_file", build_only=True
# )
#
#
# def upload_file_to_s3(file, acl="public-read"):
#     filename = secure_filename(file.filename)
#     try:
#         s3.upload_fileobj(
#             file,
#             os.getenv("AWS_BUCKET_NAME"),
#             file.filename,
#             ExtraArgs={
#                 "ACL": acl,
#                 "ContentType": file.content_type
#             }
#         )
#
#     except Exception as e:
#         # This is a catch all exception, edit this part to fit your needs.
#         print("Something Happened: ", e)
#         return e
#
#     # after upload file to s3 bucket, return filename of the uploaded file
#     return file.filename
#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
# @app.route('/uploads/shravan')
# def return_shravan():
#     return {"hello " : "shravan"}
#
#
# @app.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)
#
# @app.route('/methods/<whitespace>/<whitespace_val>/<subtitles>/<transcript>/<slideshow>', methods=['POST'])
# def methods(whitespace, whitespace_val, subtitles, transcript, slideshow):
#     if request.method == 'POST':
#         print(whitespace_val)
#
#     return '<!doctype html>'
#
# @app.route('/file', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         print(file.content_type)
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#
#             print("got file: ", file.filename)
#             print("file: ", file)
#
#             # TODO delete later; testing upload to s3 from here
#             output = upload_file_to_s3(file)
#             if output:
#                 print("success uploading to s3")
#             else:
#                 print("upload failed")
#
#             filename = secure_filename(file.filename)
#             #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''
#
# if __name__ == '__main__':
#     print('running')
#     app.secret_key = 'super secret key'
#     app.config['SESSION_TYPE'] = 'filesystem'
#     app.run(debug=True, port=8001)


import os

import boto3
from boto3 import Session
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_KEY_HERE',
    aws_secret_access_key='YOUR_SECRET_KEY_HERE',
    region_name = 'us-east-2'
)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp4', 'py', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)


def upload_file_to_s3(file, acl="public-read"):
    filename = secure_filename(file.filename)
    print(os.environ.get("AWS_BUCKET_NAME"))
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    # after upload file to s3 bucket, return filename of the uploaded file
    return file.filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/shravan')
def return_shravan():
    return {"hello " : "shravan"}


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/methods/<whitespace>/<whitespace_val>/<subtitles>/<transcript>/<slideshow>', methods=['POST'])
def methods(whitespace, whitespace_val, subtitles, transcript, slideshow):
    if request.method == 'POST':
        print(whitespace_val)

    return '<!doctype html>'


@app.route('/file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.content_type)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            print("file len", file.content_length)
            print("got file: ", file.filename)
            print("file: ", file)

            # TODO delete later; testing upload to s3 from here
            output = upload_file_to_s3(file)
            if output:
                print("success uploading to s3", output)
            else:
                print("upload failed")

            #filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    print('running')
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(debug=True, port=8001)
    app.run(host='0.0.0.0', port=8080)
    print(os.environ.get("AWS_BUCKET_NAME"))