from sqlalchemy import Column, String, create_engine, Integer, DateTime, PickleType
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime
from dotenv import load_dotenv


# load environment file           
load_dotenv()


database_path = os.getenv('DATABASE_URI')
sqlalchemy_track_modifications = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = sqlalchemy_track_modifications
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Actors
'''
class Actors(db.Model):
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  age = Column(Integer, nullable=False)
  gender = Column(String, nullable=False)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
    }

'''
Movies
'''
class Movies(db.Model):
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  release_date = Column(DateTime, default=datetime.utcnow)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date
    }
