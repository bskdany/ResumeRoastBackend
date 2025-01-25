from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/healthz')
def health_check():
    return 'OK', 200