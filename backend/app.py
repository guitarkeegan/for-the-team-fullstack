from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Team, TeamAffiliate, Roster, Player, GameSchedule, Lineup
from scripts.load_data import load_data
from handlers.team_routes import create_team_bp 
from handlers.schedule_routes import create_schedule_bp
from handlers.lineup_routes import create_lineup_bp




app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/lac_fullstack_dev')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()

app.logger.debug("loading data")
# Load data only on startup
with app.app_context():
    load_data(session)

app.register_blueprint(create_team_bp(session))
app.register_blueprint(create_schedule_bp(session))
app.register_blueprint(create_lineup_bp(session))
# If not using migrate
# Base.metadata.create_all(engine)

@app.route('/')
def index():
    teams = session.query(Team).all()
    teams_list = [{"team_id": team.team_id, "team_name": team.team_name} for team in teams]  # Convert to list of dictionaries
    return jsonify(teams_list)  # Use jsonify to return JSON response




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')