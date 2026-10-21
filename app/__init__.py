"""Team Notes: a small Flask app where a team keeps shared notes.

Anyone can read the home page. Members sign in with a password and a
one-time code, then read and write notes. Admins can list members and
remove notes.
"""
import os

from flask import Flask, Response, abort, redirect, request, session
from markupsafe import escape

from .guards import admin_required, login_required
from .store import (
    add_note,
    all_notes,
    all_users,
    check_code,
    check_password,
    delete_note,
    get_note,
    users_csv,
)

app = Flask(__name__)
app.secret_key = os.environ.get("TEAM_NOTES_SECRET_KEY", "dev-only-change-me")


@app.route("/", methods=["GET"])
def home():
    return "<h1>Team Notes</h1><p>Shared notes for a small team. <a href='/login'>Sign in</a></p>"


@app.route("/login", methods=["GET"])
def login_form():
    return (
        "<form method='post' action='/login'>"
        "<input name='email'> <input name='password' type='password'> <button>Next</button>"
        "</form>"
    )


@app.route("/login", methods=["POST"])
def login():
    user = check_password(request.form["email"], request.form["password"])
    if user is None:
        abort(401)
    session.clear()
    session["pending_user_id"] = user.id
    return redirect("/login/code")


@app.route("/login/code", methods=["POST"])
def verify_code():
    user_id = session.get("pending_user_id")
    if user_id is None or not check_code(user_id, request.form["code"]):
        abort(401)
    session.pop("pending_user_id")
    session["user_id"] = user_id
    return redirect("/notes")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")


@app.route("/notes", methods=["GET"])
@login_required
def list_notes():
    items = "".join(f"<li><a href='/notes/{n.id}'>{escape(n.title)}</a></li>" for n in all_notes())
    return f"<h1>Notes</h1><ul>{items}</ul>"


@app.route("/notes", methods=["POST"])
@login_required
def create_note():
    note = add_note(session["user_id"], request.form["title"], request.form["body"])
    return redirect(f"/notes/{note.id}")


@app.route("/notes/<int:note_id>", methods=["GET"])
@login_required
def show_note(note_id):
    note = get_note(note_id)
    if note is None:
        abort(404)
    return f"<h1>{escape(note.title)}</h1><p>{escape(note.body)}</p>"


@app.route("/admin/users", methods=["GET"])
@login_required
@admin_required
def admin_users():
    rows = "".join(f"<li>{escape(u.email)} ({u.role})</li>" for u in all_users())
    return f"<h1>Members</h1><ul>{rows}</ul>"


@app.route("/admin/notes/<int:note_id>/delete", methods=["POST"])
@login_required
@admin_required
def admin_delete_note(note_id):
    delete_note(note_id)
    return redirect("/notes")


@app.route("/admin/export", methods=["GET"])
@login_required
@admin_required
def admin_export():
    return Response(
        users_csv(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=team-members.csv"},
    )
