from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registration_code = db.Column(db.String(100), unique=True, nullable=False)
    max_sessions = db.Column(db.Integer, default=2)

    sessions = db.relationship('Session', backref='team', lazy=True)
    puzzle_states = db.relationship('PuzzleState', backref='team', lazy=True)
    attempts = db.relationship('Attempt', backref='team', lazy=True)

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_active_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    active = db.Column(db.Boolean, default=True)

class Puzzle(db.Model):
    __tablename__ = 'puzzles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # text, image, code_input
    prompt_text = db.Column(db.Text)
    image_path = db.Column(db.String(500))
    answer = db.Column(db.String(200), nullable=False)
    result_value = db.Column(db.String(100))
    unlock_message = db.Column(db.String(500))
    gold = db.Column(db.Boolean, default=False)
    unlock_condition = db.Column(db.String(500))  # JSON string

    puzzle_states = db.relationship('PuzzleState', backref='puzzle', lazy=True)
    attempts = db.relationship('Attempt', backref='puzzle', lazy=True)

class PuzzleState(db.Model):
    __tablename__ = 'puzzle_state'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzles.id'), nullable=False)
    solved = db.Column(db.Boolean, default=False)
    solved_at = db.Column(db.DateTime)
    opened = db.Column(db.Boolean, default=False)

    __table_args__ = (db.UniqueConstraint('team_id', 'puzzle_id'),)

class Attempt(db.Model):
    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzles.id'), nullable=False)
    answer_submitted = db.Column(db.Text)
    correct = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
