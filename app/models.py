from flask import url_for
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from app import db