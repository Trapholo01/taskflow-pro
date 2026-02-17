from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

db = SQLAlchemy()   # Database instance — shared across models
migrate = Migrate() # Migration instance

def create_app():
    """Application factory — creates and configures the Flask app."""
    app = Flask(__name__)

    # Configuration from environment variables
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # Initialise extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (routes)
    from app.routes.projects import projects_bp
    from app.routes.tasks    import tasks_bp
    from app.routes.health   import health_bp
    app.register_blueprint(projects_bp, url_prefix='/api/v1')
    app.register_blueprint(tasks_bp,    url_prefix='/api/v1')
    app.register_blueprint(health_bp)

    return app
