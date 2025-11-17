# Team Login Credentials

## All Team Codes

| Team # | Team Name | Registration Code | Max Sessions |
|--------|-----------|-------------------|--------------|
| 1      | Team 1    | TEAM1-2025        | 2            |
| 2      | Team 2    | TEAM2-2025        | 2            |
| 3      | Team 3    | TEAM3-2025        | 2            |
| 4      | Team 4    | TEAM4-2025        | 2            |
| 5      | Team 5    | TEAM5-2025        | 2            |
| 6      | Team 6    | TEAM6-2025        | 2            |
| 7      | Team 7    | TEAM7-2025        | 2            |
| 8      | Team 8    | TEAM8-2025        | 2            |
| 9      | Team 9    | TEAM9-2025        | 2            |
| 10     | Team 10   | TEAM10-2025       | 2            |
| 11     | Team 11   | TEAM11-2025       | 2            |
| 12     | Team 12   | TEAM12-2025       | 2            |

## How to Customize Registration Codes

Edit the `init_db()` function in `app.py` (around line 38):

```python
teams = [
    Team(id=1, name="Team 1", registration_code="YOUR-CUSTOM-CODE-1", max_sessions=2),
    Team(id=2, name="Team 2", registration_code="YOUR-CUSTOM-CODE-2", max_sessions=2),
    # ... etc
]
```

After changing codes:
1. Delete `christmas_event.db`
2. Restart the application
3. New codes will be initialized

## Puzzle Answers (Reference)

| Safe # | Puzzle Title         | Answer Type | Answer         | Result Value |
|--------|---------------------|-------------|----------------|--------------|
| 1      | What is it?         | text        | account        | 38           |
| 2      | special number      | image       | change agent   | -            |
| 3      | special calculator  | image       | white          | -            |
| 4      | What is it?         | text        | 1120           | 74           |
| 5      | special sequence    | image       | 4320           | -            |
| 6      | special square      | image       | sorry          | -            |
| 7      | Password Lock       | code        | 3874           | "Find CA"    |
| 8      | Golden Safe         | text        | saengsansung   | -            |

**Note**: Safe 8 only becomes accessible after Safe 7 is unlocked.

## Session Management

- **Max concurrent sessions per team**: 2
- **Session timeout**: 15 minutes of inactivity
- **Auto-logout**: Yes (after timeout)
- **Manual logout**: Available via logout button

## Testing Tips

1. **Test concurrent limit**:
   - Open 3 browser windows
   - Try to login as same team
   - 3rd attempt should be rejected

2. **Test puzzle progression**:
   - Login as Team 1
   - Solve Safe 1-6
   - Try to access Safe 8 (should be locked)
   - Unlock Safe 7 with code 3874
   - Safe 8 should now be accessible

3. **Test session persistence**:
   - Login and solve puzzles
   - Close browser
   - Login again (same team)
   - Progress should be saved

## Distribution to Participants

Share with teams:
- Event URL (e.g., http://your-server:5000)
- Their team number (1-12)
- Their registration code

Keep private:
- Puzzle answers
- Database access
- Server files
