from flask import abort, render_template
from werkzeug.exceptions import NotFound

from . import main_bp


@main_bp.route("/")
def index():
    return render_template('index.html')
