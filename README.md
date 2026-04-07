# Python Vulnerable Lab

This is a **deliberately vulnerable local training lab** written in Python/Flask.
It contains **only**:
- SQL Injection
- Privilege Escalation / Broken Access Control

## Files
- `app.py` - main vulnerable web app
- `init_db.py` - creates and seeds the SQLite database
- `requirements.txt` - Python dependency list

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```

Open:
```bash
http://127.0.0.1:5000/
```

## Test Accounts
- `alice / alice123`
- `bob / bob123`
- `admin / supersecret`

## Intentional Vulnerabilities

### 1) SQL Injection
The login query concatenates untrusted input directly into SQL.

Example payload for the password field:
```text
' OR '1'='1
```

### 2) Privilege Escalation
The `/admin` route trusts a user-controlled query parameter:
```text
/admin?admin=1
```
This changes the session role to `admin` and grants access.

## Notes
- Use only in a local lab or CTF-style environment.
- Do not deploy this app anywhere public.
