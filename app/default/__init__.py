from flask import Blueprint
from config import Config

default = Blueprint('cast', __name__, static_folder=Config.STATIC_FOLDER, static_url_path='')
qrs = Blueprint('images', __name__, static_folder=Config.QRS_FOLDER, static_url_path='')
documentation = Blueprint('apidocs', __name__, static_folder=Config.DOCS_FOLDER, static_url_path='')
from . import routes
