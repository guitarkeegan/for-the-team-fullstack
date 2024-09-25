from flask import Blueprint, jsonify
from flask_security import auth_required, roles_accepted
from functools import wraps

def coach_or_medical_required(f):
    @wraps(f)
    @auth_required()
    @roles_accepted('coach', 'medical')
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated

def create_team_bp(db_session):
    team_bp = Blueprint('team', __name__)

    @team_bp.route('/teams', methods=['GET'])
    @coach_or_medical_required
    def get_teams():
        teams = db_session.execute(text("SELECT * FROM teams")).fetchall()
        return jsonify([dict(team) for team in teams])

    @team_bp.route('/teams/<int:team_id>', methods=['GET'])
    @coach_or_medical_required
    def get_team(team_id):
        team = db_session.execute(text("SELECT * FROM teams WHERE team_id = :team_id"), {'team_id': team_id}).fetchone()
        if team:
            return jsonify(dict(team))
        return jsonify({"error": "Team not found"}), 404

    return team_bp