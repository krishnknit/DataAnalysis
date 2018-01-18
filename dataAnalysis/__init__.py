from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# create app
app = Flask(__name__)

app.config.from_object('config.DevelopementConfig')

# DB statement
db = SQLAlchemy(app)

# Blueprints
from dataAnalysis.histscenario.controllers import histscenario
app.register_blueprint(histscenario)

from dataAnalysis.download.controllers import download
app.register_blueprint(download)


# Logging setup
import logging
from logging.handlers import WatchedFileHandler
path = os.path.join(os.getcwd(), 'logs/dataanalysis.log')
file_handler = WatchedFileHandler(path)
file_handler.setLevel(logging.DEBUG)
formatString = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
file_handler.setFormatter(logging.Formatter(formatString))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('----------------------------data analysis startup---------------------------')

from dataAnalysis import views