from flask import Flask
import os
from dotenv import load_dotenv
from app_revolvedor import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    with app.app_context():
        print()
        db.init_db()

    return app

__version__ = '0.1.0'
app = create_app()

import app_revolvedor.routes

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.db_session.remove()