"""Init the db variable so that all files have access to the same db"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
