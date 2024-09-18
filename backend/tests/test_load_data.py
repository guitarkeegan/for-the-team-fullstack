import pytest
import json
import tempfile
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.scripts.load_data import load_json_data, load_roster, load_data
from backend.db.models import Base, Team, TeamAffiliate, Roster, Player, GameSchedule, Lineup, ContractTypeEnum, PositionEnum, LeagueLkEnum
import logging

@pytest.fixture(scope="function")
def db_session():
    # Create an in-memory SQLite database
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def create_temp_json_file(data):
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json')
    json.dump(data, temp_file)
    temp_file.close()
    return temp_file.name

def setup_database(db_session):
    # Add teams
    teams = [
        Team(team_id=1610612737, league_lk=LeagueLkEnum.NBA, team_name="Team 1", team_name_short="T1", team_nickname="T1"),
        Team(team_id=1610612738, league_lk=LeagueLkEnum.NBA, team_name="Team 2", team_name_short="T2", team_nickname="T2"),
    ]
    db_session.add_all(teams)
    db_session.flush()

    # Add team affiliates
    affiliates = [
        TeamAffiliate(id=1, nba_team_id=1610612737, nba_abrv="T1", glg_team_id=1612709921, glg_abrv="G1"),
        TeamAffiliate(id=2, nba_team_id=1610612738, nba_abrv="T2", glg_team_id=1612709922, glg_abrv="G2"),
    ]
    db_session.add_all(affiliates)
    db_session.flush()

    # Add game schedules
    games = [
        GameSchedule(game_id=1, home_id=1610612737, away_id=1610612738, home_score=100, away_score=95, game_date=datetime(2023, 1, 1, 19, 0)),
        GameSchedule(game_id=2, home_id=1610612738, away_id=1610612737, home_score=105, away_score=102, game_date=datetime(2023, 1, 2, 20, 0)),
    ]
    db_session.add_all(games)
    db_session.flush()

    # Add players
    players = [
        Player(player_id=1, first_name="Player", last_name="One"),
        Player(player_id=2, first_name="Player", last_name="Two"),
    ]
    db_session.add_all(players)
    db_session.flush()

    # Add rosters
    rosters = [
        Roster(player_id=1, team_id=1610612737, first_name="Player", last_name="One", position=PositionEnum.PG, contract_type=ContractTypeEnum.NBA),
        Roster(player_id=2, team_id=1610612738, first_name="Player", last_name="Two", position=PositionEnum.SG, contract_type=ContractTypeEnum.TWO_WAY),
    ]
    db_session.add_all(rosters)
    db_session.commit()

def test_load_json_data(db_session):
    setup_database(db_session)
    # Test data
    test_data = [
        {"teamId": 1610612739, "leagueLk": "NBA", "teamName": "New Team", "teamNameShort": "NT", "teamNickname": "Newbies"},
    ]
    temp_file = create_temp_json_file(test_data)

    # Load data
    load_json_data(db_session, temp_file, Team)

    # Verify data
    teams = db_session.query(Team).all()
    assert len(teams) == 3
    assert teams[2].team_name == "New Team"
    assert teams[2].team_name_short == "NT"
    assert teams[2].team_nickname == "Newbies"

def test_load_roster(db_session):
    setup_database(db_session)
    # Test data
    test_data = [
        {"teamId": 1610612737, "playerId": 3, "firstName": "John", "lastName": "Doe", "position": "PF", "contractType": "NBA"},
    ]
    temp_file = create_temp_json_file(test_data)

    # Load data
    load_roster(db_session, temp_file, Roster, Player)

    # Verify data
    players = db_session.query(Player).all()
    rosters = db_session.query(Roster).all()
    assert len(players) == 3
    assert len(rosters) == 3
    assert players[2].first_name == "John"
    assert rosters[2].contract_type == ContractTypeEnum.NBA
    assert rosters[2].position == PositionEnum.PF

# Add more tests as needed for other functions and edge cases