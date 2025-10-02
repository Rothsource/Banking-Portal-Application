import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    # Absolute path to Frontend folder outside BackEnd
    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))
    frontend_path = os.path.join(project_root, "Fronend")

    app = Flask(
        __name__,
        template_folder=os.path.join(frontend_path, "templetes"),  
        static_folder=os.path.join(frontend_path, "static")
    )

    app.config.from_object(Config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .routers.index import main_routes
    app.register_blueprint(main_routes, url_prefix="/")

    # Here is where you also register the user blueprint
    from .routers.user import bp as user_bp   # <- this line is causing the ImportError
    app.register_blueprint(user_bp, url_prefix="/users")

    return app
