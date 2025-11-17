from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from datetime import datetime, timedelta
import os
from models import db, Team, Session as SessionModel, Puzzle, PuzzleState, Attempt

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'christmas-secret-key-2025')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///christmas_event.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TIMEOUT_MINUTES'] = 15

db.init_app(app)

def init_db():
    """Initialize database with teams and puzzles"""
    with app.app_context():
        db.create_all()

        # Create teams if they don't exist
        if Team.query.count() == 0:
            teams = [
                Team(id=i, name=f"Team {i}", registration_code=f"TEAM{i}-2025", max_sessions=2)
                for i in range(1, 13)
            ]
            db.session.add_all(teams)

        # Create puzzles if they don't exist
        if Puzzle.query.count() == 0:
            puzzles = [
                Puzzle(id=1, title="What is it?", type="image",
                       prompt_text="What is it?",
                       image_path="/static/images/puzzle1.jpg",
                       answer="account", result_value="38"),
                Puzzle(id=2, title="special number", type="image",
                       prompt_text="Special Number",
                       image_path="/static/images/puzzle2.jpg",
                       answer="change agent"),
                Puzzle(id=3, title="special calculator", type="image",
                       prompt_text="Use the special calculator.",
                       image_path="/static/images/puzzle3.jpg",
                       answer="white"),
                Puzzle(id=4, title="What is it?", type="image",
                       prompt_text="Look at this number sequence: What comes next?",
                       image_path="/static/images/puzzle4.jpg",
                       answer="1120", result_value="74"),
                Puzzle(id=5, title="special sequence", type="image",
                       prompt_text="Decode the sequence in the image.",
                       image_path="/static/images/puzzle5.jpg",
                       answer="4320"),
                Puzzle(id=6, title="special square", type="image",
                       prompt_text="What word appears in the magic square?",
                       image_path="/static/images/puzzle6.jpg",
                       answer="sorry"),
                Puzzle(id=7, title="Password Lock", type="code_input",
                       prompt_text="Enter the 4-digit code to unlock this safe.",
                       answer="3874", unlock_message="Find CA"),
                Puzzle(id=8, title="Golden Safe", type="text",
                       prompt_text="What is the final word?",
                       answer="saengsansung", gold=True, unlock_condition='{"requires_puzzle_opened": 7}'),
            ]
            db.session.add_all(puzzles)

        db.session.commit()

def cleanup_expired_sessions():
    """Remove inactive sessions older than timeout period"""
    timeout = datetime.now() - timedelta(minutes=app.config['SESSION_TIMEOUT_MINUTES'])
    SessionModel.query.filter(
        SessionModel.active == True,
        SessionModel.last_active_at < timeout
    ).update({'active': False})
    db.session.commit()

def get_current_team():
    """Get the current team from session"""
    if 'team_id' in session:
        return db.session.get(Team, session['team_id'])
    return None

def update_session_activity():
    """Update last activity time for current session"""
    if 'session_id' in session:
        session_obj = db.session.get(SessionModel, session['session_id'])
        if session_obj:
            session_obj.last_active_at = datetime.now()
            db.session.commit()

@app.before_request
def before_request():
    """Check session validity before each request"""
    if request.endpoint and request.endpoint not in ['static', 'login', 'enter']:
        update_session_activity()
        if 'team_id' not in session:
            return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    """Display login page"""
    return render_template('login.html')

@app.route('/api/enter', methods=['POST'])
def enter():
    """Handle login with team number and registration code"""
    data = request.json
    team_num = data.get('team')
    reg_code = data.get('registration_code')

    # Validate input
    if not team_num or not reg_code:
        return jsonify({'ok': False, 'error': 'Team number and registration code are required'}), 400

    # Find team
    team = Team.query.filter_by(id=team_num, registration_code=reg_code).first()
    if not team:
        return jsonify({'ok': False, 'error': 'Invalid team number or registration code'}), 401

    # Clean up expired sessions
    cleanup_expired_sessions()

    # Check active session count for this team
    active_count = SessionModel.query.filter_by(team_id=team.id, active=True).count()
    if active_count >= team.max_sessions:
        return jsonify({'ok': False, 'error': 'Maximum number of people already connected'}), 403

    # Create new session
    new_session = SessionModel(
        team_id=team.id,
        created_at=datetime.now(),
        last_active_at=datetime.now(),
        active=True
    )
    db.session.add(new_session)
    db.session.commit()

    # Store in Flask session
    session['team_id'] = team.id
    session['session_id'] = new_session.id
    session['team_name'] = team.name

    return jsonify({'ok': True, 'team': team.id, 'team_name': team.name})

@app.route('/main')
def main():
    """Display main puzzle grid page"""
    team = get_current_team()
    if not team:
        return redirect(url_for('login'))
    return render_template('main.html', team=team)

@app.route('/api/puzzles')
def get_puzzles():
    """Get all puzzles with current team's progress"""
    team = get_current_team()
    if not team:
        return jsonify({'ok': False, 'error': 'Not authenticated'}), 401

    puzzles = Puzzle.query.order_by(Puzzle.id).all()
    result = []

    for puzzle in puzzles:
        # Get puzzle state for this team
        state = PuzzleState.query.filter_by(team_id=team.id, puzzle_id=puzzle.id).first()

        # Check if puzzle 7 is opened (for puzzle 8 unlock condition)
        puzzle7_opened = False
        if puzzle.id == 8:
            state7 = PuzzleState.query.filter_by(team_id=team.id, puzzle_id=7).first()
            puzzle7_opened = state7 and state7.opened

        puzzle_data = {
            'id': puzzle.id,
            'title': puzzle.title,
            'type': puzzle.type,
            'gold': puzzle.gold,
            'opened': state.opened if state else False,
            'solved': state.solved if state else False,
            'unlockable': puzzle7_opened if puzzle.id == 8 else True
        }
        result.append(puzzle_data)

    return jsonify(result)

@app.route('/puzzle/<int:puzzle_id>')
def puzzle_page(puzzle_id):
    """Display individual puzzle page"""
    team = get_current_team()
    if not team:
        return redirect(url_for('login'))

    puzzle = db.session.get(Puzzle, puzzle_id)
    if not puzzle:
        abort(404)

    # Check if puzzle 8 is locked
    if puzzle.id == 8:
        state7 = PuzzleState.query.filter_by(team_id=team.id, puzzle_id=7).first()
        if not (state7 and state7.opened):
            return redirect(url_for('main'))

    return render_template('puzzle.html', puzzle=puzzle, team=team)

@app.route('/api/puzzles/<int:puzzle_id>')
def get_puzzle(puzzle_id):
    """Get puzzle details"""
    team = get_current_team()
    if not team:
        return jsonify({'ok': False, 'error': 'Not authenticated'}), 401

    puzzle = db.session.get(Puzzle, puzzle_id)
    if not puzzle:
        abort(404)
    state = PuzzleState.query.filter_by(team_id=team.id, puzzle_id=puzzle.id).first()

    puzzle_data = {
        'id': puzzle.id,
        'title': puzzle.title,
        'type': puzzle.type,
        'prompt_text': puzzle.prompt_text,
        'image_path': puzzle.image_path,
        'opened': state.opened if state else False,
        'solved': state.solved if state else False,
        'result_value': puzzle.result_value if (state and state.solved) else None,
        'unlock_message': puzzle.unlock_message if (state and state.opened and puzzle.unlock_message) else None
    }

    return jsonify(puzzle_data)

@app.route('/api/puzzles/<int:puzzle_id>/submit', methods=['POST'])
def submit_answer(puzzle_id):
    """Submit answer to a puzzle"""
    team = get_current_team()
    if not team:
        return jsonify({'ok': False, 'error': 'Not authenticated'}), 401

    puzzle = db.session.get(Puzzle, puzzle_id)
    if not puzzle:
        abort(404)
    data = request.json
    answer = data.get('answer', '').strip().lower()

    # Log attempt
    attempt = Attempt(
        team_id=team.id,
        puzzle_id=puzzle.id,
        answer_submitted=answer,
        correct=False,
        submitted_at=datetime.now()
    )

    # Check answer
    correct = answer == puzzle.answer.lower()
    attempt.correct = correct
    db.session.add(attempt)

    if correct:
        # Update puzzle state
        state = PuzzleState.query.filter_by(team_id=team.id, puzzle_id=puzzle.id).first()
        if not state:
            state = PuzzleState(team_id=team.id, puzzle_id=puzzle.id)
            db.session.add(state)

        state.solved = True
        state.solved_at = datetime.now()

        # For puzzle 7, also mark as opened
        if puzzle.id == 7:
            state.opened = True

        db.session.commit()

        return jsonify({
            'ok': True,
            'correct': True,
            'message': 'Correct!',
            'result_value': puzzle.result_value,
            'unlock_message': puzzle.unlock_message
        })
    else:
        db.session.commit()
        return jsonify({
            'ok': True,
            'correct': False,
            'message': 'Incorrect. Please try again.'
        })

@app.route('/api/puzzles/<int:puzzle_id>/unlock', methods=['POST'])
def unlock_puzzle(puzzle_id):
    """Unlock puzzle 7 with code"""
    team = get_current_team()
    if not team:
        return jsonify({'ok': False, 'error': 'Not authenticated'}), 401

    puzzle = db.session.get(Puzzle, puzzle_id)
    if not puzzle:
        abort(404)
    data = request.json
    code = data.get('code', '').strip()

    # Check code
    if code == puzzle.answer:
        state = PuzzleState.query.filter_by(team_id=team.id, puzzle_id=puzzle.id).first()
        if not state:
            state = PuzzleState(team_id=team.id, puzzle_id=puzzle.id)
            db.session.add(state)

        state.opened = True
        state.solved = True
        state.solved_at = datetime.now()
        db.session.commit()

        return jsonify({
            'ok': True,
            'opened': True,
            'message': puzzle.unlock_message
        })
    else:
        return jsonify({
            'ok': True,
            'opened': False,
            'message': 'Incorrect code. Please try again.'
        })

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout current session"""
    if 'session_id' in session:
        session_obj = db.session.get(SessionModel, session['session_id'])
        if session_obj:
            session_obj.active = False
            db.session.commit()

    session.clear()
    return jsonify({'ok': True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)
