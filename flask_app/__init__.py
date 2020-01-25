from flask import Flask, Blueprint

from .commands import create_tables
from .extensions import db
from .views import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(main)

    app.cli.add_command(create_tables)

    return app