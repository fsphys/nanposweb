from flask import Blueprint
from flask_login import login_required

from .util import admin_required

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
@admin_required
def index():
    return 'admin'
