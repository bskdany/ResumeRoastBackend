from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/healthz')
def health_check():
    return 'OK', 200