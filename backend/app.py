from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Team, TeamAffiliate, Roster, Player, GameSchedule, Lineup, User
from scripts.load_data import load_data
from handlers.team_routes import create_team_bp 
from handlers.schedule_routes import create_schedule_bp
from handlers.lineup_routes import create_lineup_bp
from handlers.doc_route import create_docs_bp
from handlers.user_routes import create_user_bp
from scripts.seed_users import seed_users
from flask_bcrypt import Bcrypt
from flask_cors import CORS




app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/lac_fullstack_dev')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysuperdupersecrelkjas;dlfkj123'  # Change this to a random secret key
bcrypt = Bcrypt(app)
# Initialize SQLAlchemy
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()

app.logger.debug("loading data and seeding users...")
# Load data only on startup
with app.app_context():
    load_data(session)
    seed_users(session, User, bcrypt)

user_bp, token_required = create_user_bp(session, app)
app.register_blueprint(user_bp)
app.logger.debug("data loaded and users seeded")
# Pass token_required to other blueprint creation functions
app.register_blueprint(create_team_bp(session, token_required))
app.register_blueprint(create_schedule_bp(session, token_required))
app.register_blueprint(create_lineup_bp(session, token_required))
app.register_blueprint(create_docs_bp(session))
# If not using migrate
# Base.metadata.create_all(engine)

@app.route('/')
def index():
    teams = session.query(Team).all()
    teams_list = [{"team_id": team.team_id, "team_name": team.team_name} for team in teams]  # Convert to list of dictionaries
    return jsonify(teams_list)  # Use jsonify to return JSON response



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

