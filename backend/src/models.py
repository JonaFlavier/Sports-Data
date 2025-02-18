from sqlalchemy import Integer, Boolean, ForeignKey, String, Column, Date
from sqlalchemy.orm import relationship
from .database import Base

# define the database tables

# Venues table
class Venues(Base):
    __tablename__ = "venues"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, index = True)

    # define relationships
    games = relationship('Games', back_populates='venue') # venue can accommodate many games


# Teams table
class Teams(Base):
    __tablename__="teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    #define relationships
    home_games = relationship("Games", back_populates="home_team", foreign_keys='[Games.home_team_id]') # teams can have many home games
    away_games = relationship("Games", back_populates="away_team", foreign_keys='[Games.away_team_id]') # teams can have many away games
    simulations = relationship("Simulations", back_populates="team") # teams can have many simulations


# Games table
class Games(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    game_date = Column(Date)
    home_team_id = Column(Integer,ForeignKey('teams.id'))
    away_team_id = Column(Integer, ForeignKey('teams.id')) 

    #define relationships   
    venue = relationship("Venues", back_populates="games") # a game has a venue
    home_team = relationship("Teams", back_populates="home_games", foreign_keys=[home_team_id]) # a game has a home team
    away_team = relationship("Teams", back_populates = "away_games", foreign_keys=[away_team_id]) # a game has an away team
    

# Simulations table
class Simulations(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    simulation = Column(Integer)
    results = Column(Integer)

    #define relationships
    team = relationship("Teams", back_populates="simulations") # a game belongs to one team

