from flask import Blueprint, jsonify
from sqlalchemy import text
# Import the new validator function
from .validators import validate_month_format
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
    team_bp = Blueprint('team', __name__, url_prefix='/teams')

    # TODO: refactor of GLG data is added to game_schedule
    @team_bp.route('/', methods=['GET'])
    @coach_or_medical_required
    def get_standings():
        """
        Retrieve and return the current team standings.

        This function executes a SQL query to calculate team standings based on
        game results from the game_schedule table. It computes games played,
        wins, losses, and win percentage for each team.

        Returns:
            JSON: A list of dictionaries containing team standings information,
                  sorted by win percentage in descending order.
        """
        result = db_session.execute(text("""
        WITH team_games AS (
            -- Get home games
            SELECT
                g.game_id,
                t.team_id,
                t.team_name,
                1 AS games_played,
                CASE WHEN g.home_score > g.away_score THEN 1 ELSE 0 END AS wins,
                CASE WHEN g.home_score < g.away_score THEN 1 ELSE 0 END AS losses
            FROM game_schedule g
            JOIN teams t ON t.team_id = g.home_id

            UNION ALL

            -- Get away games
            SELECT
                g.game_id,
                t.team_id,
                t.team_name,
                1 AS games_played,
                CASE WHEN g.away_score > g.home_score THEN 1 ELSE 0 END AS wins,
                CASE WHEN g.away_score < g.home_score THEN 1 ELSE 0 END AS losses
            FROM game_schedule g
            JOIN teams t ON t.team_id = g.away_id
        )

        SELECT
            tg.team_name,
            SUM(tg.games_played) AS games_played,
            SUM(tg.wins) AS wins,
            SUM(tg.losses) AS losses,
            ROUND(SUM(tg.wins)::NUMERIC / NULLIF(SUM(tg.games_played), 0), 3) AS win_percentage
        FROM team_games tg
        GROUP BY tg.team_id, tg.team_name
        ORDER BY win_percentage DESC, tg.team_name;
        """))
        rankings = [dict(row) for row in result]
        return jsonify(rankings)

    @team_bp.route('/<string:month>', methods=['GET'])
    @coach_or_medical_required
    def get_standings_by_month(month):
        """
        Retrieve team standings for a specific month.

        Args:
            month (str): The month for which to retrieve standings, in 'YYYY-MM' format.

        Returns:
            JSON: A message indicating the standings for the specified month,
                  or an error message if the input format is invalid.
        """
        # Use the validator function
        is_valid, error = validate_month_format(month)
        if not is_valid:
            return jsonify(error), 400

        result = db_session.execute(text("""
        WITH team_games AS (
            -- Home games
            SELECT
                g.game_id,
                t.team_id,
                t.team_name,
                1 AS games_played,
                CASE WHEN g.home_score > g.away_score THEN 1 ELSE 0 END AS wins,
                CASE WHEN g.home_score < g.away_score THEN 1 ELSE 0 END AS losses,
                -- Monthly statistics using date range
                CASE WHEN g.game_date >= TO_DATE(:month, 'YYYY-MM') 
                    AND g.game_date < (TO_DATE(:month, 'YYYY-MM') + INTERVAL '1 month') THEN 1 ELSE 0 END AS games_played_in_month,
                CASE WHEN g.game_date >= TO_DATE(:month, 'YYYY-MM') 
                    AND g.game_date < (TO_DATE(:month, 'YYYY-MM') + INTERVAL '1 month') THEN 1 ELSE 0 END AS home_games_in_month,
                0 AS away_games_in_month
            FROM game_schedule g
            JOIN teams t ON t.team_id = g.home_id

            UNION ALL

            -- Away games
            SELECT
                g.game_id,
                t.team_id,
                t.team_name,
                1 AS games_played,
                CASE WHEN g.away_score > g.home_score THEN 1 ELSE 0 END AS wins,
                CASE WHEN g.away_score < g.home_score THEN 1 ELSE 0 END AS losses,
                -- Monthly statistics using date range
                CASE WHEN g.game_date >= TO_DATE(:month, 'YYYY-MM') 
                    AND g.game_date < (TO_DATE(:month, 'YYYY-MM') + INTERVAL '1 month') THEN 1 ELSE 0 END AS games_played_in_month,
                0 AS home_games_in_month,
                CASE WHEN g.game_date >= TO_DATE(:month, 'YYYY-MM') 
                    AND g.game_date < (TO_DATE(:month, 'YYYY-MM') + INTERVAL '1 month') THEN 1 ELSE 0 END AS away_games_in_month
            FROM game_schedule g
            JOIN teams t ON t.team_id = g.away_id
        )

        SELECT
            tg.team_name,
            SUM(tg.games_played) AS games_played,
            SUM(tg.wins) AS wins,
            SUM(tg.losses) AS losses,
            ROUND(SUM(tg.wins)::NUMERIC / NULLIF(SUM(tg.games_played), 0), 3) AS win_percentage,
            SUM(tg.games_played_in_month) AS games_played_in_month,
            SUM(tg.home_games_in_month) AS home_games_in_month,
            SUM(tg.away_games_in_month) AS away_games_in_month
        FROM team_games tg
        GROUP BY tg.team_id, tg.team_name
        ORDER BY games_played_in_month DESC, tg.team_name;

        """), {"month": month})

        return jsonify([dict(row) for row in result]), 200

    return team_bp
