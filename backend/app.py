from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
import os
from db.models import Team, TeamAffiliate, Roster, Player, GameSchedule, Lineup, User, Role, UserRoles
from scripts.load_data import load_data
from scripts.load_users import load_users
from handlers.team_routes import create_team_bp 
from handlers.schedule_routes import create_schedule_bp
from handlers.lineup_routes import create_lineup_bp
from handlers.doc_route import create_docs_bp
from handlers.user_routes import create_user_bp, setup_roles
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from dotenv import load_dotenv
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf  # Add generate_csrf here

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/lac_fullstack_dev')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_SAMESITE'] = 'strict'
app.config['SESSION_COOKIE_SAMESITE'] = 'strict'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
}

# Set the secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
app.config['SECURITY_TRACKABLE'] = True

if not app.config['SECRET_KEY']:
    raise ValueError("No SECRET_KEY set for Flask application")
if not app.config['SECURITY_PASSWORD_SALT']:
    raise ValueError("No SECURITY_PASSWORD_SALT set for Flask application")
# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Set up roles and load users
with app.app_context():
    db.create_all()  # Create tables
    setup_roles(user_datastore)
    load_users(user_datastore)

# Load data only on startup
with app.app_context():
    load_data(db.session)

app.register_blueprint(create_team_bp(db.session))
app.register_blueprint(create_schedule_bp(db.session))
app.register_blueprint(create_lineup_bp(db.session))
app.register_blueprint(create_docs_bp(db.session))
app.register_blueprint(create_user_bp(user_datastore))

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the LAC Fullstack API"})

@app.route('/get-csrf-token', methods=['GET'])
def get_csrf_token():
    return jsonify({'csrf_token': generate_csrf()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')