
import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp4', 'py', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

# @app.route('/methods/<whitespace>/<whitespace_val>/<subtitles>/<transcript>/<slideshow>', methods=['POST'])
# def methods(whitespace, whitespace_val, subtitles, transcript, slideshow):
#     if request.method == 'POST':
#         print(whitespace_val)
        
#     return '<!doctype html>'


@app.route('/file/<whitespace>/<whitespace_val>/<subtitles>/<transcript>/<slideshow>', methods=['GET', 'POST'])
def upload_file(whitespace, whitespace_val, subtitles, transcript, slideshow):
    if request.method == 'POST':
        # check if the post request has the file part
        print(whitespace_val)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        print(file.content_length)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response = jsonify({'some': 'data'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
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
    app.run(debug=True, port=8001)