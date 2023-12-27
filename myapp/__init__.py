# myapp/__init__.py
# myapp/__init__.py

from flask import Flask
from myapp.config import Config

app = Flask(__name__, template_folder='../templates')
app.config.from_object(Config)

from myapp import routes

