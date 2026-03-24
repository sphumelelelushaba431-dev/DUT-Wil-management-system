from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

# Create extension objects — not attached to any app yet
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Attach extensions to this app instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register Blueprints (route files)
    from app.routes.auth import auth
    from app.routes.student import student
    from app.routes.coordinator import coordinator
    from app.routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(student,     url_prefix='/student')
    app.register_blueprint(coordinator, url_prefix='/coordinator')
    app.register_blueprint(admin,       url_prefix='/admin')

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app

