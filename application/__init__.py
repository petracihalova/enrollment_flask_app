from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json 


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database created!")


@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("Database dropped!")


@app.cli.command("db_seed")
def db_seed():
    from application.models import Course
    
    with open(file="fixtures/courses.json", mode="r") as f:
        courses = json.load(f)
    for c in courses:
        course = Course(course_id=c["course_id"], title=c["title"], description=c["description"], level=c["level"], term=c["term"])
        db.session.add(course)

    db.session.commit()
    print("Database seeded!")


from application import routes