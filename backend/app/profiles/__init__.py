"""Profiles blueprint."""
from flask import Blueprint

profiles = Blueprint('profiles', __name__)

from app.profiles import routes

