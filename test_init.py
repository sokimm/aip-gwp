"""Quick test to verify database initialization"""
from app import app, init_db, Team, Puzzle

# Initialize database
init_db()

with app.app_context():
    # Check teams
    teams = Team.query.all()
    print(f"✓ Created {len(teams)} teams")
    print(f"  Sample: {teams[0].name} - Code: {teams[0].registration_code}")

    # Check puzzles
    puzzles = Puzzle.query.all()
    print(f"✓ Created {len(puzzles)} puzzles")
    print(f"  Sample: Puzzle {puzzles[0].id} - {puzzles[0].title}")

    print("\n🎄 Database initialized successfully!")
    print("Run 'python app.py' to start the server")
