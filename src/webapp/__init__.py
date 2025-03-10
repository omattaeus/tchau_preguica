from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

from src.webapp import routes