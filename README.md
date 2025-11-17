# Christmas Treasure Hunt - Event Website

A festive online puzzle game where 12 teams compete to solve 8 Christmas-themed puzzles by opening locked safes.

## Features

- **Team-based gameplay**: 12 teams with unique registration codes
- **8 Progressive Puzzles**: Mix of text, image, and code-based challenges
- **Concurrent session limit**: Maximum 2 players per team simultaneously
- **Real-time state tracking**: Progress saved and synchronized across sessions
- **Christmas-themed UI**: Festive design with snow animations
- **Mobile responsive**: Works on desktop and mobile devices

## Quick Start

### 1. Install Dependencies

```bash
python3.11 -m pip install -r requirements.txt
```

### 2. Run the Application

```bash
python3.11 app.py
```

The application will start on `http://localhost:5000`

### 3. Access the Game

1. Open your browser and navigate to `http://localhost:5000`
2. Select your team number (1-12)
3. Enter your registration code (default: `TEAM1-2025`, `TEAM2-2025`, etc.)
4. Start solving puzzles!

## Default Team Credentials

| Team Number | Registration Code |
|-------------|-------------------|
| 1           | TEAM1-2025        |
| 2           | TEAM2-2025        |
| 3           | TEAM3-2025        |
| 4           | TEAM4-2025        |
| 5           | TEAM5-2025        |
| 6           | TEAM6-2025        |
| 7           | TEAM7-2025        |
| 8           | TEAM8-2025        |
| 9           | TEAM9-2025        |
| 10          | TEAM10-2025       |
| 11          | TEAM11-2025       |
| 12          | TEAM12-2025       |

## Puzzle Answers (For Testing)

| Safe # | Answer          | Type       |
|--------|-----------------|------------|
| 1      | account         | text       |
| 2      | change agent    | image      |
| 3      | white           | image      |
| 4      | 1120            | text       |
| 5      | 4320            | image      |
| 6      | sorry           | image      |
| 7      | 3874            | code       |
| 8      | saengsansung    | text       |

**Note**: Safe 8 only unlocks after solving Safe 7.

## Game Mechanics

1. **Login**: Teams log in with their team number and registration code
2. **Main Hall**: See all 8 safes and their current status (locked/opened)
3. **Solve Puzzles**: Click on each safe to see the puzzle and submit answers
4. **Progressive Unlock**: Safe 8 (golden safe) requires Safe 7 to be opened first
5. **Session Management**: Maximum 2 team members can play simultaneously
6. **Auto-logout**: Inactive sessions automatically expire after 15 minutes

## Adding Puzzle Images

To add images for puzzles 2, 3, 5, and 6:

1. Place your image files in the `static/images/` directory
2. Name them: `puzzle2.jpg`, `puzzle3.jpg`, `puzzle5.jpg`, `puzzle6.jpg`
3. Or update the `image_path` in the database initialization (in `app.py`)

## Customization

### Change Team Registration Codes

Edit the `init_db()` function in `app.py`:

```python
teams = [
    Team(id=1, name="Team 1", registration_code="YOUR-CUSTOM-CODE", max_sessions=2),
    # ... more teams
]
```

### Modify Puzzle Content

Edit the puzzle initialization in `init_db()` function in `app.py`:

```python
Puzzle(id=1, title="Your Title", type="text",
       prompt_text="Your puzzle question",
       answer="your_answer", result_value="38")
```

### Change Session Timeout

Edit the configuration in `app.py`:

```python
app.config['SESSION_TIMEOUT_MINUTES'] = 15  # Change to desired minutes
```

## Deployment

### Deploy to Replit

1. Create a new Replit project
2. Upload all project files
3. Replit will auto-detect Flask and install dependencies
4. Click "Run" to start the application
5. Share the public URL with participants

### Deploy to Other Platforms

The application works on any platform that supports Flask:
- **Render**: Push to GitHub and connect repository
- **Railway**: Deploy directly from GitHub
- **Heroku**: Use the included requirements.txt
- **PythonAnywhere**: Upload files and configure WSGI

## Database

The application uses SQLite by default (`christmas_event.db`), which is automatically created on first run.

### Database Tables

- `teams`: Team information and registration codes
- `sessions`: Active user sessions
- `puzzles`: Puzzle definitions and answers
- `puzzle_state`: Team progress (which safes are opened/solved)
- `attempts`: Log of all answer submissions

## Security Notes

- Registration codes are stored in plain text (consider hashing for production)
- Answers are case-insensitive and trimmed automatically
- Session tokens are managed by Flask's secure session system
- Input validation prevents basic XSS and injection attacks

## Troubleshooting

### Port already in use
```bash
# Change the port in app.py:
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Database locked error
- Stop all running instances
- Delete `christmas_event.db` and restart

### Session issues
- Clear browser cookies
- Reduce session timeout in config

## License

This is an event-specific application created for educational purposes.

## Support

For issues or questions, refer to the Software Requirements Specification (SRS) document.

---

**Merry Christmas and Happy Hunting! 🎄🎁**
