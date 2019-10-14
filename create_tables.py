from flask import Flask
from models import *

DB_NAME = "postgres"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:aaron@localhost/project2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def create_tables():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        create_tables()
