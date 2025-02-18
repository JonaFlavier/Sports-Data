from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Annotated
import numpy as np
from datetime import datetime

from sqlalchemy import create_engine
from .models import Base, Venues, Teams, Simulations, Games

from .database import engine, SessionLocal
from sqlalchemy.orm import Session, aliased
from .utils import load_csv_data, get_team_simulations
import os
# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine) # create the columns in postgres

# item for retrieving the game information
class GameAnalysisResponseItem(BaseModel):
    home_team: str
    away_team: str
    venue: str
    date: str
    # analysis data
    data: List
    
class GameAnalysisReceiveItem(BaseModel):
    game_id: int # it's required
    home_team: str = None
    away_team: str = None
    venue: str = None
    date: str = None



# get db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# load csv on startup
async def load_data_on_startup(app: FastAPI):
    db = SessionLocal()
    try:
        load_csv_data(db)
        yield
    finally: 
        db.close()

# create fastapi app with lifespan manager
app = FastAPI(lifespan=load_data_on_startup)
#configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# testing api end point
@app.get("/")
def read_root():
    return{"Hello":"World with fastapi"}

# Example endpoints to verify the data.
@app.get("/venues")
def get_venues(db: Session = Depends(get_db)):
    return db.query(Venues).all()

@app.get("/simulations")
def get_simulations(db: Session = Depends(get_db)):
    return db.query(Simulations).all()

@app.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    return db.query(Teams).all()

@app.get("/games")
def get_games(db: Session = Depends(get_db)):
    # Create aliases for teams table
    home_team = aliased(Teams)
    away_team = aliased(Teams)

    # define joins (want to return the actual name of venues, home & away teams instead of just ids)
    games = (
        db.query(
            Games.id,
            Games.game_date,
            Venues.name.label("venue_name"),
            home_team.name.label("home_team_name"),
            away_team.name.label("away_team_name"),
        )
        .join(Venues, Games.venue_id == Venues.id)  # join with venues
        .join(home_team, Games.home_team_id == home_team.id)  # join with home team
        .join(away_team, Games.away_team_id == away_team.id)  # join with away team
        .all()
    )

    return [dict(game._mapping) for game in games] # converts into normal dict for json

# based on the game picked return the percentages
@app.post("/games")
def get_game_analysis(item: GameAnalysisReceiveItem, db: Session = Depends(get_db)):
    print(item)
    game_obj = db.query(Games).filter(Games.id == item.game_id).first()
    home_t = db.query(Teams).filter(Teams.id == game_obj.home_team_id).first()
    away_t = db.query(Teams).filter(Teams.id == game_obj.away_team_id).first()
    venue_t = db.query(Venues).filter(Venues.id == game_obj.venue_id).first()

    print(f"{home_t.name} vs {away_t.name} at {venue_t.name} on {str(game_obj.game_date)}")

    home_sims = get_team_simulations(db, home_t.id)
    away_sims = get_team_simulations(db, away_t.id)
    # per teams
    ''' 
    for every simulation in a team:
    
    - calculate the min max results and roughly estimate the bins
    - place the results in histogram
    - calculate win percentage
    
    '''
    # Determine bin ranges dynamically
    all_results = home_sims + away_sims
    min_result = min(all_results)
    max_result = max(all_results)
    num_bins = 15  # Adjust for finer resolution
    bins = np.linspace(min_result, max_result, num_bins + 1).astype(int).tolist()

    # Create histogram and win percentages
    home_hist, _ = np.histogram(home_sims, bins=bins)
    away_hist, _ = np.histogram(away_sims, bins=bins)

    # Convert wins to percentages
    home_win_perc = (home_hist / len(home_sims)).tolist()
    away_win_perc = (away_hist / len(away_sims)).tolist()

    response_data = {
        'home_team':home_t,
        'away_team':away_t,
        'venue':venue_t,
        "date": str(game_obj.game_date),
        "bins": [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)],  # Bin ranges
        "sim_data": [home_win_perc, away_win_perc],  # Win percentages
    }

    # return calculated percentage results
    return {"data": response_data}
