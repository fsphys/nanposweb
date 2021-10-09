from flask import Blueprint

from .products import products_bp as products_blueprint
from .users import users_bp as users_blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

admin_bp.register_blueprint(users_blueprint)
admin_bp.register_blueprint(products_blueprint)
