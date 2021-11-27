from os import path
from os import mkdir

from flask import Flask
from flask import jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.secret_key import SECRET_KEY
from app.config import test_config, get_config
from app.database import get_url

db = SQLAlchemy()
migrate = Migrate()

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
CONFIG_DIR = path.join(BASE_DIR, "config")


def create_app():
    if not path.isdir(CONFIG_DIR):
        mkdir(CONFIG_DIR)

    test_config()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    app.config['SQLALCHEMY_DATABASE_URI'] = get_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    __import__("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    for view in views.__all__:
        app.register_blueprint(blueprint=getattr(getattr(views, view), "bp"))

    access_control_allow_origin = get_config("AccessControlAllowOrigin").host

    if access_control_allow_origin == "#":
        access_control_allow_origin = "*"

    @app.after_request
    def set_header(response):
        response.headers.add("Access-Control-Allow-Origin", access_control_allow_origin)
        return response

    app.register_error_handler(404, lambda e: (jsonify({
        "status": "fail",
        "error": {
            "code": "page_not_found",
            "message": "요청한 페이지를 찾을 수 없습니다."
        }
    }), e.code))

    return app
