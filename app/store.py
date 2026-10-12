"""An in-memory store, so the demo runs with no database.

The two members are fictional. Their passwords and codes are placeholders.
"""
import hmac
from dataclasses import dataclass

from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class User:
    id: int
    email: str
    role: str
    password_hash: str
    code: str


@dataclass
class Note:
    id: int
    author_id: int
    title: str
    body: str


USERS = {
    1: User(1, "alex@example.com", "admin", generate_password_hash("example-password-1"), "000001"),
    2: User(2, "sam@example.com", "member", generate_password_hash("example-password-2"), "000002"),
}
NOTES = {1: Note(1, 1, "Welcome", "Write down what the team learns.")}


def check_password(email, password):
    for user in USERS.values():
        if user.email == email and check_password_hash(user.password_hash, password):
            return user
    return None


def check_code(user_id, code):
    user = USERS.get(user_id)
    return user is not None and hmac.compare_digest(user.code, code)


def role_of(user_id):
    user = USERS.get(user_id)
    return user.role if user else None


def all_users():
    return list(USERS.values())


def all_notes():
    return list(NOTES.values())


def get_note(note_id):
    return NOTES.get(note_id)


def add_note(author_id, title, body):
    note = Note(max(NOTES, default=0) + 1, author_id, title, body)
    NOTES[note.id] = note
    return note


def delete_note(note_id):
    if note_id in NOTES:
        del NOTES[note_id]
