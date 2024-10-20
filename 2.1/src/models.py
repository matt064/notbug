from db import db


class Task(db.Model):
    "create a new task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(250))
    done = db.Column(db.Boolean, default=False)
