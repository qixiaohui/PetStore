from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    api_key = db.Column(db.String(64), unique=True, index=True)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    image = db.Column(db.String(128), nullable=False)
    contentList = db.Column(db.Text(), nullable=True)
    imageList = db.Column(db.Text(), nullable=False)

    @property
    def url(self):
        return url_for("getPost", index=self.id)
