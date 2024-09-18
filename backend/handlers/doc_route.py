from flask import send_from_directory, Blueprint

def create_docs_bp(db_session):
    docs_bp = Blueprint('docs', __name__, url_prefix='/docs')

    @docs_bp.route('/')
    def get_docs():
        return send_from_directory('static', 'redoc-static.html')

    return docs_bp
