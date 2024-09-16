from flask import Blueprint, jsonify, request
from sqlalchemy import text

def create_lineup_bp(db_session):
    lineup_bp = Blueprint('lineup', __name__, url_prefix='/lineups')

    # url should be /lineups/wide?page_size=50&last_game_id=1&last_team_id=1&last_lineup_num=1
    @lineup_bp.route('/wide', methods=['GET'])
    def get_wide_lineups():
        # Get pagination parameters from query string
        page_size = min(int(request.args.get('page_size', 50)), 100)  # Cap at 100 items per page
        last_game_id = request.args.get('last_game_id', type=int)
        last_team_id = request.args.get('last_team_id', type=int)
        last_lineup_num = request.args.get('last_lineup_num', type=int)

        # Initialize parameters dictionary
        params = {'page_size': page_size}

        # Build the WHERE clause for keyset pagination
        where_clause = ""
        if all(v is not None for v in [last_game_id, last_team_id, last_lineup_num]):
            where_clause = """
            WHERE (game_id, team_id, lineup_num) > (:last_game_id, :last_team_id, :last_lineup_num)
            """
            params.update({
                'last_game_id': last_game_id,
                'last_team_id': last_team_id,
                'last_lineup_num': last_lineup_num
            })

        query = f"""
            WITH lineup_data AS (
                SELECT
                    l.game_id,
                    l.team_id,
                    l.lineup_num,
                    l.period,
                    l.time_in,
                    l.time_out,
                    l.player_id,
                    p.first_name,
                    p.last_name,
                    r.position,
                    ROW_NUMBER() OVER (
                        PARTITION BY l.game_id, l.team_id, l.lineup_num, l.period, l.time_in, l.time_out
                        ORDER BY
                            CASE r.position
                                WHEN 'PG' THEN 1
                                WHEN 'SG' THEN 2
                                WHEN 'SF' THEN 3
                                WHEN 'PF' THEN 4
                                WHEN 'C'  THEN 5
                                ELSE 6  -- For any other positions
                            END,
                            l.player_id  -- Secondary ordering to ensure uniqueness
                    ) AS player_num
                FROM
                    lineup l
                JOIN
                    players p ON l.player_id = p.player_id
                JOIN
                    roster r ON l.player_id = r.player_id AND l.team_id = r.team_id
                {where_clause}
            )
            SELECT
                game_id,
                team_id,
                lineup_num,
                period,
                time_in,
                time_out,
                -- Player 1
                MAX(CASE WHEN player_num = 1 THEN player_id END) AS player1_id,
                MAX(CASE WHEN player_num = 1 THEN first_name || ' ' || last_name END) AS player1_name,
                MAX(CASE WHEN player_num = 1 THEN position END) AS player1_position,
                -- Player 2
                MAX(CASE WHEN player_num = 2 THEN player_id END) AS player2_id,
                MAX(CASE WHEN player_num = 2 THEN first_name || ' ' || last_name END) AS player2_name,
                MAX(CASE WHEN player_num = 2 THEN position END) AS player2_position,
                -- Player 3
                MAX(CASE WHEN player_num = 3 THEN player_id END) AS player3_id,
                MAX(CASE WHEN player_num = 3 THEN first_name || ' ' || last_name END) AS player3_name,
                MAX(CASE WHEN player_num = 3 THEN position END) AS player3_position,
                -- Player 4
                MAX(CASE WHEN player_num = 4 THEN player_id END) AS player4_id,
                MAX(CASE WHEN player_num = 4 THEN first_name || ' ' || last_name END) AS player4_name,
                MAX(CASE WHEN player_num = 4 THEN position END) AS player4_position,
                -- Player 5
                MAX(CASE WHEN player_num = 5 THEN player_id END) AS player5_id,
                MAX(CASE WHEN player_num = 5 THEN first_name || ' ' || last_name END) AS player5_name,
                MAX(CASE WHEN player_num = 5 THEN position END) AS player5_position
            FROM
                lineup_data
            GROUP BY
                game_id,
                team_id,
                lineup_num,
                period,
                time_in,
                time_out
            ORDER BY
                game_id,
                team_id,
                lineup_num
            LIMIT :page_size
        """

        result = db_session.execute(text(query), params)
        lineups = [dict(row) for row in result]

        # Prepare the response
        response = {
            "lineups": lineups,
            "pagination": {
                "page_size": page_size,
            }
        }

        # Add next page cursor if there are more results
        if lineups:
            last_lineup = lineups[-1]
            response["pagination"]["next_cursor"] = {
                "last_game_id": last_lineup["game_id"],
                "last_team_id": last_lineup["team_id"],
                "last_lineup_num": last_lineup["lineup_num"]
            }

        return jsonify(response), 200

    # url should be /lineups/player-stints?page_size=50&last_game_date=2024-06-01&last_team_name=
    @lineup_bp.route('/player-stints', methods=['GET'])
    def get_player_stints():
        # Get pagination parameters from query string
        page_size = min(int(request.args.get('page_size', 50)), 100)  # Cap at 100 items per page
        last_game_date = request.args.get('last_game_date')
        last_team_name = request.args.get('last_team_name')
        last_player_name = request.args.get('last_player_name')
        last_period = request.args.get('last_period', type=int)
        last_stint_number = request.args.get('last_stint_number', type=int)

        # Initialize parameters dictionary
        params = {'page_size': page_size}

        # Build the WHERE clause for keyset pagination
        where_clause = ""
        if all(v is not None for v in [last_game_date, last_team_name, last_player_name, last_period, last_stint_number]):
            where_clause = """
            WHERE (gs.game_date, t.team_name, p.first_name || ' ' || p.last_name, s.period, s.stint_number) > 
            (:last_game_date, :last_team_name, :last_player_name, :last_period, :last_stint_number)
            """
            params.update({
                'last_game_date': last_game_date,
                'last_team_name': last_team_name,
                'last_player_name': last_player_name,
                'last_period': last_period,
                'last_stint_number': last_stint_number
            })

        query = f"""
        WITH player_lineups AS (
            SELECT
                l.game_id,
                l.team_id,
                l.period,
                l.player_id,
                l.time_in,
                l.time_out
            FROM
                lineup l
        ),
        player_stints AS (
            SELECT
                pl.*,
                LAG(pl.time_out) OVER (
                    PARTITION BY pl.game_id, pl.team_id, pl.player_id
                    ORDER BY pl.period, pl.time_in
                ) AS prev_time_out,
                LAG(pl.period) OVER (
                    PARTITION BY pl.game_id, pl.team_id, pl.player_id
                    ORDER BY pl.period, pl.time_in
                ) AS prev_period,
                CASE
                    WHEN LAG(pl.time_out) OVER (
                        PARTITION BY pl.game_id, pl.team_id, pl.player_id
                        ORDER BY pl.period, pl.time_in
                    ) IS NULL
                    OR pl.time_in < LAG(pl.time_out) OVER (
                        PARTITION BY pl.game_id, pl.team_id, pl.player_id
                        ORDER BY pl.period, pl.time_in
                    )
                    OR pl.period > LAG(pl.period) OVER (
                        PARTITION BY pl.game_id, pl.team_id, pl.player_id
                        ORDER BY pl.period, pl.time_in
                    ) THEN 1
                    ELSE 0
                END AS new_stint_flag
            FROM
                player_lineups pl
        ),
        player_stints_with_group AS (
            SELECT
                ps.*,
                SUM(ps.new_stint_flag) OVER (
                    PARTITION BY ps.game_id, ps.team_id, ps.player_id
                    ORDER BY ps.period, ps.time_in
                ) AS stint_number
            FROM
                player_stints ps
        ),
        stints AS (
            SELECT
                pswg.game_id,
                pswg.team_id,
                pswg.player_id,
                pswg.period,
                pswg.stint_number,
                MAX(pswg.time_in) AS stint_start_time_remaining,
                MIN(pswg.time_out) AS stint_end_time_remaining
            FROM
                player_stints_with_group pswg
            GROUP BY
                pswg.game_id,
                pswg.team_id,
                pswg.player_id,
                pswg.period,
                pswg.stint_number
        )
        SELECT
            gs.game_date,
            t.team_name AS team,
            opp.team_name AS opponent,
            p.first_name || ' ' || p.last_name AS player_name,
            s.period,
            s.stint_number,
            TO_CHAR(
                (s.stint_start_time_remaining * INTERVAL '1 second'),
                'FMMI:SS'
            ) AS stint_start_time,
            TO_CHAR(
                (s.stint_end_time_remaining * INTERVAL '1 second'),
                'FMMI:SS'
            ) AS stint_end_time
        FROM
            stints s
        JOIN
            game_schedule gs ON s.game_id = gs.game_id
        JOIN
            teams t ON s.team_id = t.team_id
        JOIN
            players p ON s.player_id = p.player_id
        JOIN
            teams opp ON opp.team_id = CASE
                WHEN s.team_id = gs.home_id THEN gs.away_id
                ELSE gs.home_id
            END
        {where_clause}
        ORDER BY
            gs.game_date,
            t.team_name,
            player_name,
            s.period,
            s.stint_number
        LIMIT :page_size
        """

        result = db_session.execute(text(query), params)
        stints = [dict(row) for row in result]

        # Prepare the response
        response = {
            "stints": stints,
            "pagination": {
                "page_size": page_size,
            }
        }

        # Add next page cursor if there are more results
        if stints:
            last_stint = stints[-1]
            response["pagination"]["next_cursor"] = {
                "last_game_date": last_stint["game_date"].isoformat(),
                "last_team_name": last_stint["team"],
                "last_player_name": last_stint["player_name"],
                "last_period": last_stint["period"],
                "last_stint_number": last_stint["stint_number"]
            }

        return jsonify(response), 200

    # url should be /lineups/stint-averages?page_size=50&last_player_name=
    @lineup_bp.route('/stint-averages', methods=['GET'])
    def stint_averages():
        # Get pagination parameters from query string
        page_size = min(int(request.args.get('page_size', 50)), 100)  # Cap at 100 items per page
        last_player_name = request.args.get('last_player_name')

        # Initialize parameters dictionary
        params = {'page_size': page_size}

        # Build the WHERE clause for keyset pagination
        where_clause = ""
        if last_player_name is not None:
            where_clause = "WHERE player_name > :last_player_name"
            params['last_player_name'] = last_player_name

        query = f"""
            WITH player_lineups AS (
                SELECT
                    l.game_id,
                    l.team_id,
                    l.period,
                    l.player_id,
                    l.time_in,
                    l.time_out
                FROM
                    lineup l
            ),
            player_stints AS (
                SELECT
                    pl.*,
                    LAG(pl.time_out) OVER (
                        PARTITION BY pl.game_id, pl.player_id, pl.period
                        ORDER BY pl.time_in DESC
                    ) AS prev_time_out,
                    CASE
                        WHEN LAG(pl.time_out) OVER (
                            PARTITION BY pl.game_id, pl.player_id, pl.period
                            ORDER BY pl.time_in DESC
                        ) IS NULL
                        OR pl.time_in < LAG(pl.time_out) OVER (
                            PARTITION BY pl.game_id, pl.player_id, pl.period
                            ORDER BY pl.time_in DESC
                        ) THEN 1
                        ELSE 0
                    END AS new_stint_flag
                FROM
                    player_lineups pl
            ),
            player_stints_with_group AS (
                SELECT
                    ps.*,
                    SUM(ps.new_stint_flag) OVER (
                        PARTITION BY ps.game_id, ps.player_id, ps.period
                        ORDER BY ps.time_in DESC
                    ) AS stint_number
                FROM
                    player_stints ps
            ),
            stints AS (
                SELECT
                    pswg.game_id,
                    pswg.player_id,
                    pswg.stint_number,
                    MAX(pswg.time_in) AS stint_start_time_remaining,
                    MIN(pswg.time_out) AS stint_end_time_remaining
                FROM
                    player_stints_with_group pswg
                GROUP BY
                    pswg.game_id,
                    pswg.player_id,
                    pswg.stint_number
            ),
            stint_durations AS (
                SELECT
                    s.*,
                    (s.stint_start_time_remaining - s.stint_end_time_remaining) AS stint_duration
                FROM
                    stints s
            ),
            player_stats AS (
                SELECT
                    p.player_id,
                    p.first_name || ' ' || p.last_name AS player_name,
                    COUNT(DISTINCT sd.game_id) AS total_games,
                    COUNT(*) AS total_stints,
                    SUM(sd.stint_duration) AS total_stint_duration
                FROM
                    stint_durations sd
                JOIN
                    players p ON sd.player_id = p.player_id
                GROUP BY
                    p.player_id,
                    p.first_name,
                    p.last_name
            )
            SELECT
                player_name,
                ROUND((total_stints::numeric / total_games), 2) AS avg_stints_per_game,
                TO_CHAR(
                    MAKE_INTERVAL(secs => (total_stint_duration::numeric / total_stints)),
                    'MI:SS'
                ) AS avg_stint_length
            FROM
                player_stats
            {where_clause}
            ORDER BY
                player_name
            LIMIT :page_size
        """

        result = db_session.execute(text(query), params)
        data = [dict(row) for row in result]

        # Prepare the response
        response = {
            "stint_averages": data,
            "pagination": {
                "page_size": page_size,
            }
        }

        # Add next page cursor if there are more results
        if data:
            last_player = data[-1]
            response["pagination"]["next_cursor"] = {
                "last_player_name": last_player["player_name"]
            }

        return jsonify(response), 200

    # url should be /lineups/win-loss-stints?page_size=50&last_player_name=
    @lineup_bp.route('/win-loss-stints', methods=['GET'])
    def win_loss_stints():
        # Get pagination parameters from query string
        page_size = min(int(request.args.get('page_size', 50)), 100)  # Cap at 100 items per page
        last_player_name = request.args.get('last_player_name')

        # Initialize parameters dictionary
        params = {'page_size': page_size}

        # Build the WHERE clause for keyset pagination
        where_clause = ""
        if last_player_name is not None:
            where_clause = "WHERE player_name > :last_player_name"
            params['last_player_name'] = last_player_name

        query = f"""
            WITH player_lineups AS (
                SELECT
                    l.game_id,
                    l.team_id,
                    l.period,
                    l.player_id,
                    l.time_in,
                    l.time_out
                FROM
                    lineup l
            ),
            player_stints AS (
                SELECT
                    pl.*,
                    LAG(pl.time_out) OVER (
                        PARTITION BY pl.game_id, pl.player_id, pl.period
                        ORDER BY pl.time_in DESC
                    ) AS prev_time_out,
                    CASE
                        WHEN LAG(pl.time_out) OVER (
                            PARTITION BY pl.game_id, pl.player_id, pl.period
                            ORDER BY pl.time_in DESC
                        ) IS NULL
                        OR pl.time_in < LAG(pl.time_out) OVER (
                            PARTITION BY pl.game_id, pl.player_id, pl.period
                            ORDER BY pl.time_in DESC
                        ) THEN 1
                        ELSE 0
                    END AS new_stint_flag
                FROM
                    player_lineups pl
            ),
            player_stints_with_group AS (
                SELECT
                    ps.*,
                    SUM(ps.new_stint_flag) OVER (
                        PARTITION BY ps.game_id, ps.player_id, ps.period
                        ORDER BY ps.time_in DESC
                    ) AS stint_number
                FROM
                    player_stints ps
            ),
            stints AS (
                SELECT
                    pswg.game_id,
                    pswg.team_id,
                    pswg.player_id,
                    pswg.stint_number,
                    MAX(pswg.time_in) AS stint_start_time_remaining,
                    MIN(pswg.time_out) AS stint_end_time_remaining
                FROM
                    player_stints_with_group pswg
                GROUP BY
                    pswg.game_id,
                    pswg.team_id,
                    pswg.player_id,
                    pswg.stint_number
            ),
            stint_durations AS (
                SELECT
                    s.*,
                    (s.stint_start_time_remaining - s.stint_end_time_remaining) AS stint_duration,
                    gs.home_id,
                    gs.away_id,
                    gs.home_score,
                    gs.away_score,
                    CASE
                        WHEN (s.team_id = gs.home_id AND gs.home_score > gs.away_score)
                        OR (s.team_id = gs.away_id AND gs.away_score > gs.home_score) THEN 'Win'
                        ELSE 'Loss'
                    END AS result
                FROM
                    stints s
                JOIN
                    game_schedule gs ON s.game_id = gs.game_id
            ),
            player_stats AS (
                SELECT
                    p.player_id,
                    p.first_name || ' ' || p.last_name AS player_name,
                    -- Total stats
                    COUNT(DISTINCT sd.game_id) AS total_games,
                    COUNT(*) AS total_stints,
                    SUM(sd.stint_duration) AS total_stint_duration,
                    -- Wins stats
                    COUNT(DISTINCT CASE WHEN sd.result = 'Win' THEN sd.game_id END) AS total_games_wins,
                    COUNT(CASE WHEN sd.result = 'Win' THEN 1 END) AS total_stints_wins,
                    SUM(CASE WHEN sd.result = 'Win' THEN sd.stint_duration ELSE 0 END) AS total_stint_duration_wins,
                    -- Losses stats
                    COUNT(DISTINCT CASE WHEN sd.result = 'Loss' THEN sd.game_id END) AS total_games_losses,
                    COUNT(CASE WHEN sd.result = 'Loss' THEN 1 END) AS total_stints_losses,
                    SUM(CASE WHEN sd.result = 'Loss' THEN sd.stint_duration ELSE 0 END) AS total_stint_duration_losses
                FROM
                    stint_durations sd
                JOIN
                    players p ON sd.player_id = p.player_id
                GROUP BY
                    p.player_id,
                    p.first_name,
                    p.last_name
            )
            SELECT
                player_name,
                -- All games
                total_games,
                ROUND(total_stints::numeric / NULLIF(total_games, 0), 2) AS avg_stints_per_game,
                TO_CHAR(
                    MAKE_INTERVAL(secs => total_stint_duration::numeric / NULLIF(total_stints, 0)),
                    'MI:SS'
                ) AS avg_stint_length,
                -- Wins
                total_games_wins,
                ROUND(total_stints_wins::numeric / NULLIF(total_games_wins, 0), 2) AS avg_stints_per_game_wins,
                TO_CHAR(
                    MAKE_INTERVAL(secs => total_stint_duration_wins::numeric / NULLIF(total_stints_wins, 0)),
                    'MI:SS'
                ) AS avg_stint_length_wins,
                -- Losses
                total_games_losses,
                ROUND(total_stints_losses::numeric / NULLIF(total_games_losses, 0), 2) AS avg_stints_per_game_losses,
                TO_CHAR(
                    MAKE_INTERVAL(secs => total_stint_duration_losses::numeric / NULLIF(total_stints_losses, 0)),
                    'MI:SS'
                ) AS avg_stint_length_losses,
                -- Differences (Wins - Losses)
                ROUND(
                    (total_stints_wins::numeric / NULLIF(total_games_wins, 0))
                    - (total_stints_losses::numeric / NULLIF(total_games_losses, 0)),
                    2
                ) AS avg_stints_per_game_diff,
                CASE
                    WHEN (total_stint_duration_wins::numeric / NULLIF(total_stints_wins, 0)) > (total_stint_duration_losses::numeric / NULLIF(total_stints_losses, 0))
                    THEN TO_CHAR(
                        MAKE_INTERVAL(secs =>
                            (total_stint_duration_wins::numeric / NULLIF(total_stints_wins, 0))
                            - (total_stint_duration_losses::numeric / NULLIF(total_stints_losses, 0))
                        ),
                        'MI:SS'
                    )
                    ELSE '-' || TO_CHAR(
                        MAKE_INTERVAL(secs =>
                            (total_stint_duration_losses::numeric / NULLIF(total_stints_losses, 0))
                            - (total_stint_duration_wins::numeric / NULLIF(total_stints_wins, 0))
                        ),
                        'MI:SS'
                    )
                END AS avg_stint_length_diff
            FROM
                player_stats
            {where_clause}
            ORDER BY
                player_name
            LIMIT :page_size
        """

        result = db_session.execute(text(query), params)
        data = [dict(row) for row in result]

        # Prepare the response
        response = {
            "win_loss_stints": data,
            "pagination": {
                "page_size": page_size,
            }
        }

        # Add next page cursor if there are more results
        if data:
            last_player = data[-1]
            response["pagination"]["next_cursor"] = {
                "last_player_name": last_player["player_name"]
            }

        return jsonify(response), 200

    return lineup_bp
