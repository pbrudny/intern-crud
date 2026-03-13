"""Profiles blueprint."""
from flask import Blueprint

profiles = Blueprint('profiles', __name__, template_folder='templates')

from app.profiles import routes

