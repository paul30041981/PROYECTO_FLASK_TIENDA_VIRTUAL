from app import app
from flask import render_template, send_from_directory
from flask_login import login_required
from pathlib import Path
from app.middleware import administrator


@app.route('/')
@login_required
@administrator
def index():
    return render_template('auth/login.html')

# @app.route('/uploads/<filename>')
# def uploads(filename):
#     root_dir = Path(__file__).parent.parent.parent
#     upload_dir = root_dir / 'uploads'
#     return send_from_directory(upload_dir, filename)

# @app.before_request
# def before_request():
#     controller = MenuController()
#     controller.get_all()
