
import os, csv
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from app import app

ALLOWED_EXTENSIONS = set(['csv','md','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# UPLOAD_FOLDER = os.path.basename('uploads')
UPLOAD_FOLDER = '/home/ubuntu/doc_class/uploads'
# UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 

# from app.predict.predictNB import predictNB
from app.train.predictNB import predictNB

@app.route('/upload', methods=['POST'])
def upload_file():
	file = request.files['image']
	if allowed_file(file.filename):
		filename = secure_filename(file.filename)
		f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
		file.save(f)
		predictNB(f)
	return render_template('index_results.html')
	

from app.train.trainNB import trainNB


@app.route('/train', methods=['POST'])
def upload_train():
	file = request.files['image']
	if allowed_file(file.filename):
		filename = secure_filename(file.filename)
		f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	
	    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
		file.save(f)
		trainNB(f)
		f = os.path.join(app.config['UPLOAD_FOLDER'], "train.csv")
		file.save(f) # this does not work
		
	return render_template('index_results_train.html')	

@app.route('/download1', methods=['GET', 'POST'])
def download1_file():
    return redirect(url_for('download_csv', filename = 'devresult.csv'))
@app.route('/download2', methods=['GET', 'POST'])
def download2_file():
    return redirect(url_for('download_image',filename='devconfusion.png'))
@app.route('/download3', methods=['GET', 'POST'])
def download3_file():
    return redirect(url_for('download_csv', filename = 'result.csv'))
@app.route('/download4', methods=['GET', 'POST'])
def download4_file():
    return redirect(url_for('download_image', filename='confusion.png'))

@app.route('/download1/<filename>')
@app.route('/download3/<filename>')
def download_image(filename):
    return send_from_directory(directory=  app.config['IMAGE_FOLDER'], filename = filename)

@app.route('/download2/<filename>')
@app.route('/download4/<filename>')
def download_csv(filename):
    return send_from_directory(directory = app.config['RESULT_FOLDER'],filename = filename)
