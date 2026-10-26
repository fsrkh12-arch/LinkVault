import os
import secrets
import sqlite3
from functools import wraps
from urllib.parse import urlparse

from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", secrets.token_hex(32)),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    MAX_CONTENT_LENGTH=16 * 1024,
)

DATABASE = os.path.join(app.root_path, "database.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def create_tables():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            tag TEXT,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    db.commit()


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def valid_csrf():
    return secrets.compare_digest(session.get("csrf_token", ""), request.form.get("csrf_token", ""))


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


def valid_url(value):
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


@app.context_processor
def add_csrf_token():
    return {"csrf_token": csrf_token}


@app.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    db = get_db()
    if request.method == "POST":
        if not valid_csrf():
            flash("Please try submitting the form again.")
            return redirect(url_for("dashboard"))

        title = request.form.get("title", "").strip()
        link_url = request.form.get("url", "").strip()
        tag = request.form.get("tag", "").strip()

        if not title or not link_url:
            flash("A title and a link are required.")
        elif len(title) > 100 or len(tag) > 30:
            flash("Keep titles under 100 characters and tags under 30.")
        elif not valid_url(link_url):
            flash("Use a complete http:// or https:// link.")
        else:
            db.execute(
                "INSERT INTO links (title, url, tag, user_id) VALUES (?, ?, ?, ?)",
                (title, link_url, tag or None, session["user_id"]),
            )
            db.commit()
            flash("Link saved.")
        return redirect(url_for("dashboard"))

    search = request.args.get("search", "").strip()
    tag = request.args.get("tag", "").strip()
    query = "SELECT * FROM links WHERE user_id = ?"
    values = [session["user_id"]]
    if search:
        query += " AND (title LIKE ? OR url LIKE ? OR tag LIKE ?)"
        values.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    if tag:
        query += " AND tag = ?"
        values.append(tag)
    query += " ORDER BY created_at DESC, id DESC"

    links = db.execute(query, values).fetchall()
    tags = db.execute(
        "SELECT DISTINCT tag FROM links WHERE user_id = ? AND tag IS NOT NULL ORDER BY tag",
        (session["user_id"],),
    ).fetchall()
    return render_template("dashboard.html", links=links, tags=tags, search=search, selected_tag=tag)


@app.post("/delete/<int:link_id>")
@login_required
def delete_link(link_id):
    if not valid_csrf():
        flash("Please try again.")
        return redirect(url_for("dashboard"))
    db = get_db()
    db.execute("DELETE FROM links WHERE id = ? AND user_id = ?", (link_id, session["user_id"]))
    db.commit()
    flash("Link deleted.")
    return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not valid_csrf():
            flash("Please try submitting the form again.")
            return redirect(url_for("register"))
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        if not 3 <= len(username) <= 40 or not username.replace("_", "").isalnum():
            flash("Usernames need 3–40 letters, numbers, or underscores.")
        elif len(password) < 8:
            flash("Passwords need at least 8 characters.")
        elif password != confirmation:
            flash("Passwords do not match.")
        else:
            try:
                get_db().execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                get_db().commit()
            except sqlite3.IntegrityError:
                flash("That username is already taken.")
            else:
                flash("Account created. Please log in.")
                return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not valid_csrf():
            flash("Please try submitting the form again.")
            return redirect(url_for("login"))
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Incorrect username or password.")
        else:
            session.clear()
            session["user_id"] = user["id"]
            csrf_token()
            return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.post("/logout")
@login_required
def logout():
    if valid_csrf():
        session.clear()
    return redirect(url_for("login"))


with app.app_context():
    create_tables()


if __name__ == "__main__":
    app.run(debug=True)
