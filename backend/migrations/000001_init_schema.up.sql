-- forgoing optimitic locking, assuming infrequent updates
-- {"teamId":1610612737,"leagueLk":"NBA","teamName":"Atlanta Hawks","teamNameShort":"ATL","teamNickname":"Hawks"}
-- consider using emums for team_name, team_name_short, and team_nickname
CREATE TYPE league_lk AS ENUM ('NBA', 'GLG');

CREATE TABLE IF NOT EXISTS teams (
    team_id BIGINT PRIMARY KEY,
    league_lk league_lk NOT NULL,
    team_name TEXT NOT NULL,
    team_name_short TEXT NOT NULL,
    team_nickname TEXT NOT NULL
);

-- {"nba_teamId":1610612751,"nba_abrv":"BKN","glg_teamId":1612709921.0,"glg_abrv":"LIN"}
-- there is not always an NBA affiliate for each G League team
-- one team is null, the .0 is left off of the teams table
-- one team is null
CREATE TABLE IF NOT EXISTS team_affiliates (
    id BIGSERIAL PRIMARY KEY,
    nba_team_id BIGINT NOT NULL,
    nba_abrv TEXT NOT NULL, 
    glg_team_id BIGINT,
    glg_abrv TEXT
);

-- {"player_id":1626246,"first_name":"Boban","last_name":"Marjanovic"}
CREATE TABLE IF NOT EXISTS players (
    player_id BIGINT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TYPE contract_type AS ENUM ('NBA', 'GLG', 'TWO_WAY');
CREATE TYPE position AS ENUM ('PG', 'SG', 'SF', 'PF', 'C');

-- players on roster are not necessarily in the player table, unless I change that
-- going to assume this is not for historical rosters, but current
-- {"team_id":1610612737,"player_id":202083,"first_name":"Wesley","last_name":"Matthews","position":"SG","contract_type":"NBA"}
CREATE TABLE IF NOT EXISTS roster (
    player_id BIGINT NOT NULL REFERENCES players(player_id),
    team_id BIGINT REFERENCES teams(team_id),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    "position" "position" NOT NULL,
    contract_type contract_type NOT NULL,
    PRIMARY KEY (player_id, team_id)
);


--{"game_id":1,"home_id":1610612752,"home_score":112,"away_id":1610612750,"away_score":106,"game_date":"2024-01-01 15:00:00"}
CREATE TABLE IF NOT EXISTS game_schedule (
    game_id BIGINT PRIMARY KEY,
    home_id BIGINT REFERENCES teams(team_id),
    away_id BIGINT REFERENCES teams(team_id),
    home_score INTEGER NOT NULL,
    away_score INTEGER NOT NULL,
    game_date TIMESTAMP NOT NULL,
    UNIQUE (home_id, away_id, game_date)
);

-- {"team_id":1610612737,"player_id":1629027,"lineup_num":1,"period":1,"time_in":720.0,"time_out":456.0,"game_id":17}

CREATE TABLE IF NOT EXISTS lineup (
    id BIGSERIAL PRIMARY KEY,
    team_id BIGINT REFERENCES teams(team_id),
    player_id BIGINT REFERENCES players(player_id),
    game_id BIGINT NOT NULL REFERENCES game_schedule(game_id),
    lineup_num INTEGER NOT NULL,
    period INTEGER NOT NULL, 
    time_in NUMERIC(4, 1) NOT NULL,
    time_out NUMERIC(4, 1) NOT NULL,
    CHECK (time_out <= time_in),
    UNIQUE (team_id, player_id, game_id, period, time_in, lineup_num)
);

CREATE INDEX idx_lineup_game_id ON lineup (game_id);
CREATE INDEX idx_lineup_player_id ON lineup (player_id);
CREATE INDEX idx_lineup_team_id ON lineup (team_id);