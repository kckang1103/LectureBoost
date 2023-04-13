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
from silence import cut_silence

from emails import send_links
from multiprocessing import Process, Queue

# load environment variables
load_dotenv()

# connect to s3 bucket
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=Config(region_name='us-east-2', signature_version='s3v4')
)

UPLOAD_FOLDER = os.getenv('UPLOADS_FOLDER')
SLIDES_FILE = UPLOAD_FOLDER + 'slides.pdf'
TEXT_FROM_SLIDES_FILE = UPLOAD_FOLDER + 'textFromSlides.txt'
TRANSCRIPT_FILE = UPLOAD_FOLDER + 'transcription.txt'
ALLOWED_EXTENSIONS = {'mp4'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule(
    '/uploads/<name>', endpoint='download_file', build_only=True
)

# Generate presigned url so it can be displayed in browser
def make_signed_pdf_url(key):
    url = s3.generate_presigned_url(
    ClientMethod='get_object', 
    Params={
        'Bucket': os.getenv('AWS_BUCKET_NAME'), 
        'Key': key, 'ResponseContentDisposition': f'inline; filename={key}', 
        'ResponseContentType' : 'application/pdf'
        },
    ExpiresIn=36000)
    return url


# Generate presigned url so it can be displayed in browser
def make_signed_txt_url(key):
    url = s3.generate_presigned_url(
    ClientMethod='get_object', 
    Params={
        'Bucket': os.getenv('AWS_BUCKET_NAME'), 
        'Key': key, 'ResponseContentDisposition': f'inline; filename={key}', 
        'ResponseContentType' : 'text/plain'
        },
    ExpiresIn=36000)
    return url


# upload a pdf file to the s3 bucket
def upload_pdf_to_s3(filename):
    resource = boto3.resource(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    resource.Object('lecture-boost', filename).upload_file(filename)
    url = make_signed_pdf_url(filename)
    return url


# upload regular file object
def upload_file_to_s3(file, filename):
    try:
        s3.upload_fileobj(
            file,
            os.getenv('AWS_BUCKET_NAME'),
            filename,
        )

    except Exception as e:
        print('Something Happened: ', e)
        return

    # after upload file to s3 bucket, return filename of the uploaded file
    location = s3.get_bucket_location(Bucket=os.getenv('AWS_BUCKET_NAME'))['LocationConstraint']
    print(location)
    url = 'https://%s.s3.%s.amazonaws.com/%s' % (os.getenv('AWS_BUCKET_NAME'), location, filename)
    print(url)

    return url


# run the silence removing script with specified minimum duration and file name
def run_whitespace(file_name, minimum_duration, response):
    print('whitespace is true')
    file_name = cut_silence(file_name, float(minimum_duration))
    with open(file_name, 'rb') as f:
        print("to s3")
        response_from_s3 = upload_file_to_s3(f, file_name)
        print("past s3")
        response['video'] = response_from_s3
        if response_from_s3:
            print('success uploading to s3', response_from_s3)
        else:
            print('upload failed')

    return response, file_name


# run the transcript generating script
def run_transcript(file_name, queue):
    print('transcript is true')
    transcribe(file_name, UPLOAD_FOLDER)
    response = queue.get()
    with open(TRANSCRIPT_FILE, 'rb') as f:
        response_from_s3 = upload_file_to_s3(f, TRANSCRIPT_FILE)
        signed_url = make_signed_txt_url(TRANSCRIPT_FILE)
        response['transcript'] = signed_url
        if signed_url:
            print('success uploading transcript to s3', response_from_s3)
        else:
            print('transcript upload failed')
    queue.put(response)
    return response


# run the slideshow generating script
def run_slideshow(file_name, queue):
    print('slideshow is true')
    generate_slides(file_name, UPLOAD_FOLDER)
    response = queue.get()

    with open(SLIDES_FILE, 'rb') as f, open(TEXT_FROM_SLIDES_FILE, 'rb') as f2:
        response_from_s3 = upload_file_to_s3(f, SLIDES_FILE)
        response['slides'] = upload_pdf_to_s3(SLIDES_FILE)
        if response_from_s3:
            print('success uploading slides to s3', response_from_s3)
        else:
            print('slides upload failed')
        response_from_s3 = upload_file_to_s3(f2, TEXT_FROM_SLIDES_FILE)
        response['textFromSlides'] = response_from_s3
        if response_from_s3:
            print('success uploading text fr slide to s3', response_from_s3)
        else:
            print('text from slide upload failed')
    queue.put(response)
    return response


# email links to the given email address
def email_links(response, send_email, email):
    if send_email == 'true':
        links = []
        links.append(response['slides'])
        links.append(response['video'])
        links.append(response['transcript'])
        print(email)
        send_links(links, email)


# run the chosen processes on the given video file
def process_file(file, whitespace, minimum_duration, slideshow, subtitles, transcript):
    response = {
        'transcript': '',
        'video': '',
        'textFromSlides': '',
        'slides': ''
    }
    # just to pass to methods for testing reasons
    queue = Queue()
    queue.put("response")

    filename = UPLOAD_FOLDER + file.filename
    if whitespace == 'true':
        response, filename = run_whitespace(filename, minimum_duration, response)
        print("after whitespace")
    if subtitles == 'true':
        print('subtitles is true')
        add_subtitles(filename, UPLOAD_FOLDER)
    if transcript == 'true':
        print("transcript")
        response = run_transcript(filename, queue)
    if slideshow == 'true':
        response = run_slideshow(filename, queue)

    return response


# run the chosen processes on the given video file concurrently
def multiproc_file(file, whitespace, minimum_duration, slideshow, subtitles, transcript):
    response = {
        'transcript': '',
        'video': '',
        'textFromSlides': '',
        'slides': ''
    }

    procs = []
    queue = Queue()
    queue.put(response)

    filename = UPLOAD_FOLDER + file.filename
    if whitespace == 'true':
        # whitespace must always be run first if chosen
        response, filename = run_whitespace(filename, minimum_duration, response)
    if subtitles == 'true':
        print('subtitles is true')
        proc = Process(target=add_subtitles, args=(filename, UPLOAD_FOLDER))
        procs.append(proc)
    if transcript == 'true':
        proc = Process(target=run_transcript, args=(filename, queue))
        procs.append(proc)
    if slideshow == 'true':
        proc = Process(target=run_slideshow, args=(filename, queue))
        procs.append(proc)

    for proc in procs:
        proc.start()
    
    for proc in procs:
        proc.join()

    multiproc_response = queue.get()

    response['slides'] = multiproc_response['slides']
    response['textFromSlides'] = multiproc_response['textFromSlides']
    response['transcript'] = multiproc_response['transcript']

    return response

# check if file extension is in allowed format list
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# route to test if backend is up and running
@app.route('/uploads/test')
def return_shravan():
    return {'test ': 'I am running',
            'test2 ': 'I am running'}


# send file from uploads folder
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


# endpoint for processing files
@app.route('/file/<whitespace>/<minimum_duration>/<subtitles>/<transcript>/<slideshow>/<send_email>/<email>', methods=['GET', 'POST'])
def upload_file(whitespace, minimum_duration, subtitles, transcript, slideshow, send_email, email):
    response = {
        'transcript': '',
        'video': '',
        'textFromSlides': '',
        'slides': ''
    }

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file_in = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file_in.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file_in and allowed_file(file_in.filename):
            filename = secure_filename(file_in.filename)
            file_in.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # process the file and generate an http response to send back with links
            response = multiproc_file(file_in, whitespace, minimum_duration, slideshow, subtitles, transcript)
            # email links if selected
            email_links(response, send_email, email)

    final_response = jsonify(response)
    final_response.headers.add('Access-Control-Allow-Origin', '*')
    print('final response: \n', final_response.headers)

    return final_response


if __name__ == '__main__':
    print('running')
    app.secret_key = os.getenv('APP_SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(threaded=True, host='0.0.0.0', port=8080)