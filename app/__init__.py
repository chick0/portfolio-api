from os import environ

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from app.secret_key import SECRET_KEY

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # add CORS Headers with extension
    CORS(
        app=app,
        origins=[
            x.strip()
            for x in environ['CORS_ORIGIN'].split(";") if len(x.strip()) != 0
        ],
        allow_headers=[
            "content-type",
            "x-auth"
        ]
    )

    __import__("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    for view in views.__all__:
        app.register_blueprint(blueprint=getattr(getattr(views, view), "bp"))

    # Info for crawler
    @app.get("/robots.txt")
    def robots():
        return getattr(__import__("flask"), "Response")(
            "\n".join([
                "User-agent: *",
                "Disallow: /",
                "Allow: /api/project",
                "Allow: /api/projects",
            ]),
            mimetype="text/plain"
        )

    from app.utils import error

    @app.errorhandler(404)
    @app.errorhandler(405)
    def error_handler(http_error):
        return error(
            code=http_error.code,
            message="올바른 요청이 아닙니다."
        )

    return app
