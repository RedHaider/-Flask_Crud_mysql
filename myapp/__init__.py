# myapp/__init__.py
# myapp/__init__.py

from flask import Flask, render_template, request, redirect, url_for 
from myapp.config import Config
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='../templates')
app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'localhost'  # Replace with your MySQL host
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

from myapp import routes

