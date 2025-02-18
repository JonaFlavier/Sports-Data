import pandas as pd
from sqlalchemy.orm import Session
from .models import Venues, Simulations, Games, Teams
from datetime import datetime

# table checks if empty
def table_is_empty(db: Session, table):
    count = db.query(table).count()
    return count==0

# load venues data
def load_venues_data(db:Session, base_path:str):
    # load the venues
    venues_df = pd.read_csv(f"{base_path}/venues.csv")
    # print(venues_df)
    venues = []
    for index, row in venues_df.iterrows():
        print(f"inside venues:{index} {row}")
        venue = Venues(id=row['venue_id'], name=row['venue_name'])
        venues.append(venue)

    db.add_all(venues)
    db.commit()

# load simulations data
def load_simulations_data(db:Session, base_path:str):
    # load the simulations
    simulations_df = pd.read_csv(f"{base_path}/simulations.csv")
    simulations = []

    for index, row in simulations_df.iterrows():
        print(f"inside simulations: {index}: {row}")
        team_id = row['team_id']
        # check if team is in Teams db first and if not add them to table
        team_exists = db.query(Teams).filter(Teams.name == row['team']).first()
        if not team_exists:
            # add the team
            team = Teams(id=int(team_id), name=row['team']) 
            db.add(team)
            db.commit()
            db.refresh(team)

        simulation = Simulations(
            team_id = team_id,
            simulation = int(row['simulation_run']),
            results=int(row['results'])
        )
        simulations.append(simulation)
    
    # add all simulations into table
    db.add_all(simulations)
    db.commit()

# load games data
def load_games_data(db:Session, base_path:str):
    # load the games
    games_df = pd.read_csv(f"{base_path}/games.csv")
    games=[]

    for index, row in games_df.iterrows():
        print(f"inside games:{index} {row}")
        # find the venue, home and away team ids 
        home_team = db.query(Teams).filter(Teams.name == row['home_team']).first()
        away_team = db.query(Teams).filter(Teams.name == row['away_team']).first()
        venue = db.query(Venues).filter(Venues.id == row['venue_id']).first()

        game = Games(
            home_team_id = home_team.id,
            away_team_id = away_team.id,
            game_date = datetime.strptime(row['date'], "%Y-%m-%d").date(),
            venue_id = venue.id
        )
        games.append(game)
    # add all games to table
    db.add_all(games)
    db.commit()

def load_csv_data(db: Session):
    base_url_path = "/backend/data"
    # load the venues
    if table_is_empty(db, Venues):
        load_venues_data(db, base_url_path)
    else: 
        print("Venues table already populated")
    
    # load the simulations
    if table_is_empty(db, Simulations):
        load_simulations_data(db, base_url_path)
    else:
        print("Simulations table already populated")

    # load the games
    if table_is_empty(db, Games):
        load_games_data(db, base_url_path)
    else:
        print("Games table already populated")

##|  |##################################################################################################
def get_team_simulations(db:Session, team_id):
    tmp_sims = db.query(Simulations).filter(Simulations.team_id == team_id).all()
    return [sim.results for sim in tmp_sims]  # Extracting the results