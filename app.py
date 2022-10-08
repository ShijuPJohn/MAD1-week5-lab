import os.path

from flask import Flask

from application.config import ProductionConfig, LocalDevelopmentConfig
from application.models import db


def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    return app


app = create_app()

from application.controllers import *

if __name__ == "__main__":
    app.run(debug=True)
