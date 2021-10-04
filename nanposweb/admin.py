from flask import Blueprint
from flask_login import login_required

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def index():
    return 'admin'
