from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from flask_login import login_required, logout_user, login_user

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def index():
    return 'admin'
