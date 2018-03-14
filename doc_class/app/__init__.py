# dummyapp/app/__init__.py
from flask import Flask
app = Flask(__name__)
from app import views
MODEL_FOLDER = '/home/ubuntu/doc_class/app/models'
app.config['MODEL_FOLDER'] = MODEL_FOLDER
IMAGE_FOLDER = '/home/ubuntu/doc_class/app/templates/images'
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
MODEL_FOLDER = '/home/ubuntu/doc_class/app/result'
app.config['RESULT_FOLDER'] = MODEL_FOLDER