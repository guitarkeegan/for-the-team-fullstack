import json
import ijson
from helpers.json_to_db_helpers import camel_to_snake, convert_json_keys_to_snake_case, check_contract_type
from sqlalchemy.dialects.postgresql import insert
import re
import logging
from db.models import Team, TeamAffiliate, Roster, Player, GameSchedule, Lineup

# Load JSON data into the database
def load_json_data(session, file_path, model_class):

    with open(file_path, 'r') as file:
        data = json.load(file)
        for record in data:
            snake_case_record = convert_json_keys_to_snake_case(record)  # Convert keys
            session.merge(model_class(**snake_case_record))  # Use merge to handle inserts/updates
        session.commit()

def load_roster(session, file_path, model_roster, model_player, batch_size=1000):
    existing_players = {player.player_id for player in session.query(model_player.player_id).all()}

    existing_roster_entries = {
        (roster.player_id, roster.team_id) 
        for roster in session.query(model_roster.player_id, model_roster.team_id).all()
    }

    count_inserts = 0
    roster_records = []
    player_records = []

    with open(file_path, 'r') as file:
        for record in ijson.items(file, 'item'):
            snake_case_record = convert_json_keys_to_snake_case(record)
            player_id = snake_case_record['player_id']
            team_id = snake_case_record['team_id']
            snake_case_record['contract_type'] = check_contract_type(snake_case_record['contract_type'])

            # Check if the roster entry exists
            if (player_id, team_id) not in existing_roster_entries:
                # Add roster record to batch
                roster_records.append(model_roster(**snake_case_record))
                existing_roster_entries.add((player_id, team_id))  # Update memory with new roster entry

            # Check if the player exists in memory, if not, add to the player_records
            if player_id not in existing_players:
                player_records.append(model_player(
                    player_id=player_id, 
                    first_name=snake_case_record['first_name'], 
                    last_name=snake_case_record['last_name']
                ))
                existing_players.add(player_id)  # Update memory with the new player
                count_inserts += 1

            # Insert player records in batches
            if len(player_records) >= batch_size:
                session.bulk_save_objects(player_records)
                session.commit()
                player_records.clear()

            # Insert roster records in batches
            if len(roster_records) >= batch_size:
                session.bulk_save_objects(roster_records)
                session.commit()
                roster_records.clear()

        # Insert any remaining records after the loop
        if player_records:
            session.bulk_save_objects(player_records)
            session.commit()
            player_records.clear()

        if roster_records:
            session.bulk_save_objects(roster_records)
            session.commit()
            roster_records.clear()

    logging.info(f"Inserted {count_inserts} new players")



# Load all the required data
def load_data(session):

    load_json_data(session, 'dev_test_data/team.json', Team)
    load_json_data(session, 'dev_test_data/team_affiliate.json', TeamAffiliate)
    load_json_data(session, 'dev_test_data/game_schedule.json', GameSchedule)
    load_json_data(session, 'dev_test_data/player.json', Player)
    load_roster(session, 'dev_test_data/roster.json', Roster, Player)

    # for the lineups
    def load_large_json(session, file_path, model_class, batch_size=1000):
        conflict_fields = ['team_id', 'player_id', 'game_id', 'period', 'time_in', 'lineup_num']
        records_batch = []
        count_inserts = 0

        with open(file_path, 'r') as file:
            for record in ijson.items(file, 'item'):
                snake_case_record = convert_json_keys_to_snake_case(record)
                records_batch.append(snake_case_record)

                if len(records_batch) >= batch_size:
                    upsert_records(session, model_class, records_batch, conflict_fields)
                    count_inserts += len(records_batch)
                    records_batch.clear()

            # Process any remaining records
            if records_batch:
                upsert_records(session, model_class, records_batch, conflict_fields)
                count_inserts += len(records_batch)

        logging.info("Finished processing large JSON file")
        logging.info(f"Processed {count_inserts} records")




    load_large_json(session, 'dev_test_data/lineup.json', Lineup)

#------- Helper functions -------

from sqlalchemy.dialects.postgresql import insert

def upsert_records(session, model_class, records, conflict_fields):
    stmt = insert(model_class).values(records)
    
    # Exclude primary keys and conflict fields from the update
    update_dict = {c.name: c for c in stmt.excluded if c.name not in conflict_fields and not c.primary_key}
    
    stmt = stmt.on_conflict_do_update(
        index_elements=conflict_fields,
        set_=update_dict
    )
    session.execute(stmt)
    session.commit()




def can_combine_rows(prev_row, current_row):
    """
    Checks if the current row can be combined with the previous row.
    Conditions:
    - Same player_id, team_id, game_id, period.
    - time_out of prev_row equals time_in of current_row.
    """
    return (
        prev_row['player_id'] == current_row['player_id'] and
        prev_row['team_id'] == current_row['team_id'] and
        prev_row['game_id'] == current_row['game_id'] and
        prev_row['period'] == current_row['period'] and
        prev_row['time_out'] == current_row['time_in']
    )