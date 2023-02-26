import os
from dotenv import load_dotenv

import boto3
from botocore.client import Config
from flask import Flask, flash, request, redirect, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename

from generateSlides import generate_slides
from subtitles import add_subtitles
from transcribe import transcribe
from whiteSpace import removeWhiteSpace

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=Config(region_name='us-east-2', signature_version='s3v4')
    
    
)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp4', 'py', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

def make_signed_pdf_url(key):
    url = s3.generate_presigned_url(
    ClientMethod='get_object', 
    Params={
        'Bucket': os.getenv('AWS_BUCKET_NAME'), 
        'Key': key, f"ResponseContentDisposition": "inline; filename={key}", 
        "ResponseContentType" : "application/pdf"
        },
    ExpiresIn=3600)
    return url


def upload_pdf_to_s3(filename):
    resource = boto3.resource(
        "s3",
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    resource.Object("lecture-boost", filename).upload_file(filename)
    location = s3.get_bucket_location(Bucket=os.getenv("AWS_BUCKET_NAME"))['LocationConstraint']
    url = "https://%s.s3.%s.amazonaws.com/%s" % (os.getenv("AWS_BUCKET_NAME"), location, filename)
    url = make_signed_pdf_url(filename)
    return url


def upload_file_to_s3(file, filename, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            filename,
        )

    except Exception as e:
        print("Something Happened: ", e)
        return

    # after upload file to s3 bucket, return filename of the uploaded file
    location = s3.get_bucket_location(Bucket=os.getenv("AWS_BUCKET_NAME"))['LocationConstraint']
    print(location)
    # url = "https://s3-%s.amazonaws.com/%s/%s" % (location, os.environ.get("AWS_BUCKET_NAME"), filename)
    url = "https://%s.s3.%s.amazonaws.com/%s" % (os.getenv("AWS_BUCKET_NAME"), location, filename)
    print(url)

    return url


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/shravan')
def return_shravan():
    return {"hello ": "shravan",
            "hi ": "I am shravan"}


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/file/<whitespace>/<whitespace_val>/<subtitles>/<transcript>/<slideshow>', methods=['GET', 'POST'])
def upload_file(whitespace, whitespace_val, subtitles, transcript, slideshow):
    response = {
        "transcript": "",
        "video": "",
        "textFromSlides": "",
        "slides": ""
    }

    if request.method == 'POST':
        # check if the post request has the file part

        print(whitespace_val)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if whitespace == "true":
                print("whitespace is true")
                removeWhiteSpace(folderName="uploads/", videoName=file.filename)
                white_space_filename = "uploads/" + file.filename[:-4] + "_cut.mp4"
                if subtitles == "true":
                    print("subtitles is true")
                    add_subtitles(white_space_filename)
                if transcript == "true":
                    print("transcript is true")
                    transcribe(white_space_filename)
                    with open("uploads/transcription.txt", "rb") as f:
                        response_from_s3 = upload_file_to_s3(f, "uploads/transcription.txt")
                        response["transcript"] = response_from_s3
                        if response_from_s3:
                            print("success uploading transcript to s3", response_from_s3)
                        else:
                            print("transcript upload failed")
                if slideshow == "true":
                    print("slideshow is true")
                    generate_slides(white_space_filename)
                    with open("uploads/slides.pdf", "rb") as f:
                        with open("uploads/textFromSlides.txt", "rb") as f2:
                            response_from_s3 = upload_file_to_s3(f, "uploads/slides.pdf")
                            response["slides"] = upload_pdf_to_s3("uploads/slides.pdf")
                            if response_from_s3:
                                print("success uploading slides to s3", response_from_s3)
                            else:
                                print("slides upload failed")
                            response_from_s3 = upload_file_to_s3(f2, "uploads/textFromSlides.txt")
                            response["textFromSlides"] = response_from_s3
                            if response_from_s3:
                                print("success uploading text fr slide to s3", response_from_s3)
                            else:
                                print("text from slide upload failed")

                with open(white_space_filename, "rb") as f:
                    response_from_s3 = upload_file_to_s3(f, white_space_filename)
                    response["video"] = response_from_s3
                    if response_from_s3:
                        print("success uploading to s3", response_from_s3)
                    else:
                        print("upload failed")
            else:
                print("whitespace is false")

                no_white_space_filename = "uploads/" + file.filename
                if subtitles == "true":
                    print("make subtitles")
                    add_subtitles(no_white_space_filename)
                    file_to_upload = open(no_white_space_filename, "r")
                    response_from_s3 = upload_file_to_s3(file_to_upload, no_white_space_filename)
                    response["video"] = response_from_s3
                    if response_from_s3:
                        print("success uploading to s3", response_from_s3)
                    else:
                        print("upload failed")
                if transcript == "true":
                    transcribe(no_white_space_filename)
                    transcription_to_upload = open("uploads/transcription.txt", "rb")
                    response_from_s3 = upload_file_to_s3(transcription_to_upload, "uploads/transcription.txt")
                    response["transcript"] = response_from_s3
                    if response_from_s3:
                        print("success uploading transcript to s3", response_from_s3)
                    else:
                        print("transcript upload failed")
                if slideshow == "true":
                    generate_slides(no_white_space_filename)
                    slides_to_upload = open("uploads/slides.pdf", "rb")
                    text_from_slides_to_upload = open("uploads/textFromSlides.txt", "rb")
                    response_from_s3 = upload_file_to_s3(slides_to_upload, "uploads/slides.pdf")
                    response["slides"] = str(upload_pdf_to_s3("uploads/slides.pdf"))
                    if response_from_s3:
                        print("success uploading slides to s3", response_from_s3)
                    else:
                        print("slides upload failed")
                    response_from_s3 = upload_file_to_s3(text_from_slides_to_upload, "uploads/textFromSlides.txt")
                    response["textFromSlides"] = response_from_s3
                    if response_from_s3:
                        print("success uploading text fr slide to s3", response_from_s3)
                    else:
                        print("text from slide upload failed")

    print("response: \n", response)
    final_response = jsonify(response)
    final_response.headers.add('Access-Control-Allow-Origin', '*')
    # if slideshow:
    #     final_response.headers.add(f"Content-Disposition", f"inline; filename=\"{response['slides']}\"")
    print("final response: \n", final_response.headers)

    return final_response


if __name__ == '__main__':
    print('running')
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(debug=True, port=8001)
    app.run(threaded=True, host='0.0.0.0', port=8080)
    print(os.environ.get("AWS_BUCKET_NAME"))
