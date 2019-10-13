from flask import Flask

app = Flask(__name__)

from app import views
from app import admin_views
from app.myFunc import parser
from app.myFunc import AdminParser
