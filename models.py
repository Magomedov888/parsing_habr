from flask_sqlalchemy import SQLAlchemy
import json
from flask import Flask
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///habr_posts.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)


class Post(db.Model):
    __tablename__ = 'habr_posts'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    responses = db.Column(db.String, nullable=False)
    views = db.Column(db.String, nullable=False)
    published_at = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)


def create():

    with open("jobs.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:

        tags = ""
        for tag in item['tags']:
            tags = tag + ", "

        post = Post(url=item['url'], title=item['title'],
                    price=item['price'], responses=item['responses'],
                    views=item['views'], published_at=item['published_at'], tags=tags)
        db.session.add(post)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        create()