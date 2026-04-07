from flask import Flask, request, session, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "dev-secret-key"
DB_PATH = os.path.join(os.path.dirname(__file__), "lab.db")

LOGIN_TEMPLATE = """
<!doctype html>
<title>Vuln Lab</title>
<h2>Login</h2>
<form method="post">
  <input name="username" placeholder="username">
  <input name="password" type="password" placeholder="password">
  <button type="submit">Login</button>
</form>
<p>{{ message }}</p>
<p>Try: alice / alice123 or bob / bob123</p>
"""

PROFILE_TEMPLATE = """
<!doctype html>
<title>Profile</title>
<h2>Welcome {{ user }}</h2>
<p>Role: {{ role }}</p>
<p><a href="/admin">Go to admin page</a></p>
<p><a href="/logout">Logout</a></p>
"""

ADMIN_TEMPLATE = """
<!doctype html>
<title>Admin</title>
<h2>Admin Panel</h2>
<p>Visible only to admins. Current user: {{ user }}</p>
<p><a href="/users">List users</a></p>
<p><a href="/logout">Logout</a></p>
"""

USERS_TEMPLATE = """
<!doctype html>
<title>Users</title>
<h2>Users</h2>
<ul>
{% for row in rows %}
  <li>{{ row[0] }} - {{ row[1] }}</li>
{% endfor %}
</ul>
<p><a href="/admin">Back</a></p>
"""


def get_db():
    return sqlite3.connect(DB_PATH)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Vulnerability 1: SQL Injection
        # Intentionally unsafe string concatenation for training purposes.
        query = f"SELECT username, role FROM users WHERE username = '{username}' AND password = '{password}'"

        conn = get_db()
        cur = conn.cursor()
        try:
            row = cur.execute(query).fetchone()
        finally:
            conn.close()

        if row:
            session['user'] = row[0]
            session['role'] = row[1]
            return redirect(url_for('profile'))
        return render_template_string(LOGIN_TEMPLATE, message='Invalid credentials')

    return render_template_string(LOGIN_TEMPLATE, message='')


@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string(PROFILE_TEMPLATE, user=session['user'], role=session.get('role', 'user'))


@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Vulnerability 2: Privilege Escalation / Broken Access Control
    # Trusts a user-controlled query parameter to elevate role.
    if request.args.get('admin') == '1':
        session['role'] = 'admin'

    if session.get('role') != 'admin':
        return 'Forbidden', 403

    return render_template_string(ADMIN_TEMPLATE, user=session['user'])


@app.route('/users')
def users():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        return 'Forbidden', 403

    conn = get_db()
    cur = conn.cursor()
    try:
        rows = cur.execute("SELECT username, role FROM users").fetchall()
    finally:
        conn.close()

    return render_template_string(USERS_TEMPLATE, rows=rows)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
