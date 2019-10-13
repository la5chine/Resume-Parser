import os
#import magic
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from json import dumps, load

from app.myFunc import parser


ALLOWED_EXTENSIONS = set(['pdf'])

my_path = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(my_path, "\\templates\\Files")
UPLOAD_FOLDER = "C:/Users/Chaker khachine/Desktop/Automn2k19/pdf_Flask/app/templates/Files"

app.secret_key = 'sdvsdvvefef'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024




def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')



@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print('******',request.form)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            with open(os.path.join(my_path, "templates/Files/data.txt"), 'r') as json_file:
                data = load(json_file)
                l = len(data)
            file.save("C:/Users/Chaker khachine/Desktop/Automn2k19/pdf_Flask/app/templates/Files/"+ str(l) +".pdf")
            text = parser.maketxt((os.path.join(app.config['UPLOAD_FOLDER'], str(l)+ ".pdf" )))
            res = parser.getreslt(text)
            info = parser.getinfo(res , request.form , filename )
            flash('File successfully uploaded')
            return render_template('public/preview.html' , res = info)
        else:
            flash('Allowed file type is pdf only')
            return redirect(request.url)
