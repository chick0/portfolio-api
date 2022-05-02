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
    CORS(app)

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

    return app
