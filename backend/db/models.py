from sqlalchemy import create_engine, Column, BigInteger, String, Integer, Enum, Numeric, ForeignKey, TIMESTAMP, CheckConstraint, Text, UniqueConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_security import UserMixin, RoleMixin
import enum
from sqlalchemy.sql import func

Base = declarative_base()

# Define Enums


class LeagueLkEnum(enum.Enum):
    NBA = 'NBA'
    GLG = 'GLG'


class ContractTypeEnum(enum.Enum):
    NBA = 'NBA'
    GLG = 'GLG'
    TWO_WAY = 'TWO_WAY'


class PositionEnum(enum.Enum):
    PG = 'PG'
    SG = 'SG'
    SF = 'SF'
    PF = 'PF'
    C = 'C'
    UNKNOWN = 'UNKNOWN'


class Role(Base, RoleMixin):
    __tablename__ = 'roles'
    id = Column(BigInteger, primary_key=True)
    name = Column(Text, unique=True)
    description = Column(Text)


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
    last_login_at = Column(TIMESTAMP, nullable=False,
                           server_default=func.current_timestamp())
    current_login_at = Column(TIMESTAMP)
    last_login_ip = Column(Text)
    current_login_ip = Column(Text)
    login_count = Column(Integer, default=0)
    fs_uniquifier = Column(Text, unique=True, nullable=False)
    confirmed_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=func.current_timestamp())

    roles = relationship('Role', secondary='user_roles', backref='users')


class UserRoles(Base):
    __tablename__ = 'user_roles'
    user_id = Column('user_id', BigInteger, ForeignKey(
        'users.id'), primary_key=True)
    role_id = Column('role_id', BigInteger, ForeignKey(
        'roles.id'), primary_key=True)


class Team(Base):
    __tablename__ = 'teams'
    team_id = Column(BigInteger, primary_key=True)
    league_lk = Column(Enum(LeagueLkEnum), nullable=False)
    team_name = Column(String, nullable=False)
    team_name_short = Column(String, nullable=False)
    team_nickname = Column(String, nullable=False)

    # Relationship with Roster
    roster_entries = relationship("Roster", back_populates="team")
    home_games = relationship(
        "GameSchedule", foreign_keys="[GameSchedule.home_id]", back_populates="home_team")
    away_games = relationship(
        "GameSchedule", foreign_keys="[GameSchedule.away_id]", back_populates="away_team")


class TeamAffiliate(Base):
    __tablename__ = 'team_affiliates'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nba_team_id = Column(BigInteger, nullable=False)
    nba_abrv = Column(String, nullable=False)
    glg_team_id = Column(BigInteger, nullable=True)
    glg_abrv = Column(String, nullable=True)


class Player(Base):
    __tablename__ = 'players'
    player_id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    # Relationship with Roster
    roster_entries = relationship("Roster", back_populates="player")
    lineup_entries = relationship("Lineup", back_populates="player")


class Roster(Base):
    __tablename__ = 'roster'
    player_id = Column(BigInteger, ForeignKey(
        'players.player_id'), primary_key=True)
    team_id = Column(BigInteger, ForeignKey('teams.team_id'), primary_key=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    position = Column(Enum(PositionEnum), nullable=False)  # Changed to Enum
    contract_type = Column(Enum(ContractTypeEnum),
                           nullable=False)  # Changed to Enum

    # Relationships
    player = relationship("Player", back_populates="roster_entries")
    team = relationship("Team", back_populates="roster_entries")

    def __repr__(self):
        return f"<Roster(player_id={self.player_id}, team_id={self.team_id}, position={self.position}, contract_type={self.contract_type})>"


class GameSchedule(Base):
    __tablename__ = 'game_schedule'
    game_id = Column(BigInteger, primary_key=True)
    home_id = Column(BigInteger, ForeignKey('teams.team_id'), nullable=False)
    away_id = Column(BigInteger, ForeignKey('teams.team_id'), nullable=False)
    home_score = Column(Integer, nullable=False)
    away_score = Column(Integer, nullable=False)
    game_date = Column(TIMESTAMP, nullable=False)

    # Relationships
    home_team = relationship("Team", foreign_keys=[
                             home_id], back_populates="home_games")
    away_team = relationship("Team", foreign_keys=[
                             away_id], back_populates="away_games")
    lineup_entries = relationship("Lineup", back_populates="game")


class Lineup(Base):
    __tablename__ = 'lineup'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    team_id = Column(BigInteger, ForeignKey('teams.team_id'))
    player_id = Column(BigInteger, ForeignKey('players.player_id'))
    game_id = Column(BigInteger, ForeignKey('game_schedule.game_id'))
    lineup_num = Column(Integer, nullable=False)
    period = Column(Integer, nullable=False)
    time_in = Column(Numeric(4, 1), nullable=False)
    time_out = Column(Numeric(4, 1), nullable=False)

    # Check Constraint
    __table_args__ = (
        CheckConstraint('time_out <= time_in', name='check_time'),
        UniqueConstraint('team_id', 'player_id', 'game_id',
                         'period', 'time_in', 'lineup_num', name='uq_lineup')
    )

    # Relationships
    team = relationship("Team")
    player = relationship("Player", back_populates="lineup_entries")
    game = relationship("GameSchedule", back_populates="lineup_entries")
