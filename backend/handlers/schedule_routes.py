from flask import Blueprint, jsonify
from sqlalchemy import text
from .validators import validate_date_range
import re
from datetime import datetime

def create_schedule_bp(db_session):
    schedule_bp = Blueprint('schedule', __name__, url_prefix='/schedule')

    @schedule_bp.route('/most-b2b', methods=['GET'])
    def most_back_to_back_games():

        result = db_session.execute(text("""
            WITH team_games AS (
                SELECT
                    t.team_id,
                    t.team_name,
                    g.game_id,
                    DATE(g.game_date) AS game_date,  -- Convert to DATE to remove time component
                    CASE WHEN g.home_id = t.team_id THEN 'home' ELSE 'away' END AS location
                FROM
                    teams t
                JOIN
                    game_schedule g ON t.team_id = g.home_id OR t.team_id = g.away_id
            ),
            team_games_with_lag AS (
                SELECT
                    tg.*,
                    LAG(game_date) OVER (PARTITION BY team_id ORDER BY game_date) AS prev_game_date,
                    LAG(location) OVER (PARTITION BY team_id ORDER BY game_date) AS prev_location
                FROM
                    team_games tg
            ),
            back_to_backs AS (
                SELECT
                    team_id,
                    team_name,
                    -- Total back-to-back games
                    COUNT(*) FILTER (
                        WHERE prev_game_date IS NOT NULL AND game_date - prev_game_date = 1
                    ) AS total_back_to_backs,
                    -- Home-Home back-to-back games
                    COUNT(*) FILTER (
                        WHERE prev_game_date IS NOT NULL AND game_date - prev_game_date = 1 AND prev_location = 'home' AND location = 'home'
                    ) AS home_home_b2b,
                    -- Away-Away back-to-back games
                    COUNT(*) FILTER (
                        WHERE prev_game_date IS NOT NULL AND game_date - prev_game_date = 1 AND prev_location = 'away' AND location = 'away'
                    ) AS away_away_b2b,
                    -- Home-Away back-to-back games
                    COUNT(*) FILTER (
                        WHERE prev_game_date IS NOT NULL AND game_date - prev_game_date = 1 AND prev_location = 'home' AND location = 'away'
                    ) AS home_away_b2b,
                    -- Away-Home back-to-back games
                    COUNT(*) FILTER (
                        WHERE prev_game_date IS NOT NULL AND game_date - prev_game_date = 1 AND prev_location = 'away' AND location = 'home'
                    ) AS away_home_b2b
                FROM
                    team_games_with_lag
                GROUP BY
                    team_id,
                    team_name
            )

            SELECT
                team_name,
                total_back_to_backs,
                home_home_b2b,
                away_away_b2b,
                home_away_b2b,
                away_home_b2b
            FROM
                back_to_backs
            ORDER BY
                total_back_to_backs DESC,
                team_name;
                                         """))
        
        return jsonify([dict(row) for row in result]), 200

    @schedule_bp.route('/most-rest/<string:start_date>/<string:end_date>', methods=['GET'])
    def most_rest(start_date, end_date):
        # Use the validator function
        is_valid, error = validate_date_range(start_date, end_date)
        if not is_valid:
            return jsonify(error), 400

        result = db_session.execute(text("""
            WITH team_games AS (
                SELECT
                    t.team_id,
                    t.team_name,
                    g.game_id,
                    DATE(g.game_date) AS game_date  -- Convert to DATE to remove time component
                FROM
                    teams t
                JOIN
                    game_schedule g ON t.team_id = g.home_id OR t.team_id = g.away_id
                WHERE
                    g.game_date BETWEEN :start_date AND :end_date
            ),
            team_games_with_lag AS (
                SELECT
                    tg.*,
                    LAG(game_date) OVER (
                        PARTITION BY team_id
                        ORDER BY game_date
                    ) AS prev_game_date
                FROM
                    team_games tg
            ),
            team_rest_days AS (
                SELECT
                    team_id,
                    team_name,
                    prev_game_date,
                    game_date,
                    (game_date - prev_game_date) AS rest_days
                FROM
                    team_games_with_lag
                WHERE
                    prev_game_date IS NOT NULL
            ),
            team_max_rest_with_games AS (
                SELECT
                    trd.*,
                    ROW_NUMBER() OVER (
                        PARTITION BY trd.team_id
                        ORDER BY trd.rest_days DESC, trd.prev_game_date
                    ) AS rn
                FROM
                    team_rest_days trd
                    JOIN (
                        SELECT
                            team_id,
                            MAX(rest_days) AS max_rest_days
                        FROM
                            team_rest_days
                        GROUP BY
                            team_id
                    ) mrd ON trd.team_id = mrd.team_id
                    AND trd.rest_days = mrd.max_rest_days
            )
            SELECT
                team_name,
                rest_days AS max_rest_days,
                TO_CHAR(prev_game_date, 'Dy, DD Mon YYYY') AS game1_date,
                TO_CHAR(game_date, 'Dy, DD Mon YYYY') AS game2_date
            FROM
                team_max_rest_with_games
            WHERE
                rn = 1
            ORDER BY
                max_rest_days DESC,
                team_name;
                                         """), {'start_date': start_date, 'end_date': end_date})
        
        return jsonify([dict(row) for row in result]), 200

    @schedule_bp.route('/most-3-in-4s/<string:start_date>/<string:end_date>', methods=['GET'])
    def most_3_in_4s(start_date, end_date):

        is_valid, error = validate_date_range(start_date, end_date)
        if not is_valid:
            return jsonify(error), 400

        result = db_session.execute(text("""
            WITH team_games AS (
                SELECT
                    t.team_id,
                    t.team_name,
                    DATE(g.game_date) AS game_date,
                    ROW_NUMBER() OVER (
                        PARTITION BY t.team_id
                        ORDER BY DATE(g.game_date)
                    ) AS rn
                FROM
                    teams t
                JOIN
                    game_schedule g ON t.team_id = g.home_id OR t.team_id = g.away_id
                WHERE
                    DATE(g.game_date) BETWEEN :start_date AND :end_date
            ),
            three_in_four_sequences AS (
                SELECT
                    tg1.team_id,
                    tg1.team_name,
                    tg1.game_date AS game1_date,
                    tg2.game_date AS game2_date,
                    tg3.game_date AS game3_date,
                    tg3.game_date - tg1.game_date AS total_days
                FROM
                    team_games tg1
                JOIN
                    team_games tg2 ON tg1.team_id = tg2.team_id AND tg2.rn = tg1.rn + 1
                JOIN
                    team_games tg3 ON tg1.team_id = tg3.team_id AND tg3.rn = tg1.rn + 2
                WHERE
                    tg3.game_date - tg1.game_date <= 3  -- Corrected condition
            ),
            non_overlapping_sequences AS (
                SELECT
                    *,
                    ROW_NUMBER() OVER (
                        PARTITION BY team_id
                        ORDER BY game1_date
                    ) AS seq_num
                FROM
                    three_in_four_sequences
            ),
            filtered_sequences AS (
                SELECT
                    nos.*
                FROM
                    non_overlapping_sequences nos
                LEFT JOIN
                    non_overlapping_sequences nos_prev ON nos.team_id = nos_prev.team_id AND nos.seq_num = nos_prev.seq_num + 1
                WHERE
                    nos_prev.game3_date IS NULL OR nos.game1_date > nos_prev.game3_date
            ),
            three_in_four_counts AS (
                SELECT
                    team_id,
                    team_name,
                    COUNT(*) AS three_in_four_count
                FROM
                    filtered_sequences
                GROUP BY
                    team_id,
                    team_name
            )
            SELECT
                team_name,
                three_in_four_count
            FROM
                three_in_four_counts
            ORDER BY
                three_in_four_count DESC,
                team_name;

  

                                         """), {'start_date': start_date, 'end_date': end_date})
        
        return jsonify([dict(row) for row in result]), 200

    return schedule_bp