from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

from dataAnalysis import views