# Project Structure

```
aip-gwp/
├── app.py                          # Main Flask application
├── models.py                       # Database models (SQLAlchemy)
├── requirements.txt                # Python dependencies
├── run.sh                          # Quick start script
├── setup_alias.sh                  # Python alias helper
├── test_init.py                    # Database initialization test
│
├── templates/                      # HTML templates
│   ├── login.html                  # Login page
│   ├── main.html                   # Puzzle grid/main hall
│   └── puzzle.html                 # Individual puzzle page
│
├── static/                         # Static files
│   ├── style.css                   # Christmas-themed CSS
│   └── images/                     # Puzzle images directory
│       └── README.txt              # Instructions for adding images
│
├── christmas_event.db              # SQLite database (auto-created)
│
├── README.md                       # Full documentation
├── QUICKSTART.md                   # Quick start guide
├── PROJECT_STRUCTURE.md            # This file
└── srs (software requirements specification).rtf  # Original requirements
```

## Key Files

### Backend (Python/Flask)
- **app.py**: Main application with routes, authentication, puzzle logic
- **models.py**: Database schema (Teams, Sessions, Puzzles, PuzzleState, Attempts)

### Frontend (HTML/CSS/JS)
- **templates/login.html**: Team login interface
- **templates/main.html**: Main puzzle grid with real-time updates
- **templates/puzzle.html**: Individual puzzle solving page
- **static/style.css**: Christmas-themed styling with snow animations

### Configuration
- **requirements.txt**: Flask and SQLAlchemy dependencies
- **run.sh**: Automated startup script
- **setup_alias.sh**: Python version alias helper

## Database Schema

### Tables
1. **teams**: Team information and registration codes
2. **sessions**: Active user sessions (concurrent limit tracking)
3. **puzzles**: Puzzle definitions, answers, and metadata
4. **puzzle_state**: Per-team progress (opened/solved status)
5. **attempts**: Answer submission log

## API Endpoints

### Authentication
- `POST /api/enter`: Login with team number and code
- `POST /api/logout`: End current session

### Game State
- `GET /api/puzzles`: Get all puzzles with team progress
- `GET /api/puzzles/{id}`: Get specific puzzle details

### Puzzle Solving
- `POST /api/puzzles/{id}/submit`: Submit answer to puzzle
- `POST /api/puzzles/{id}/unlock`: Unlock Safe 7 with code

## Features Implemented

✅ Team-based authentication (12 teams)
✅ Concurrent session limit (max 2 per team)
✅ 8 progressive puzzles (text, image, code types)
✅ Real-time state synchronization
✅ Safe 7 → Safe 8 unlock dependency
✅ Session timeout (15 min inactivity)
✅ Christmas-themed UI with animations
✅ Mobile responsive design
✅ Answer validation (case-insensitive)
✅ Progress tracking and logging

## How to Run

**Option 1: Quick Start Script**
```bash
./run.sh
```

**Option 2: Manual**
```bash
python3.11 -m pip install -r requirements.txt
python3.11 app.py
```

**Option 3: With Alias**
```bash
source setup_alias.sh
python app.py
```

Access at: **http://localhost:5000**

## Deployment Options

- **Replit**: Upload all files, run directly
- **Render/Railway**: Deploy from Git repository
- **Local Network**: Share your local IP for LAN access
- **Cloud VPS**: Deploy on any Python-compatible server
