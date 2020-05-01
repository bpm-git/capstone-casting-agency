import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from app import create_app
from models import setup_db


# load env
load_dotenv()

database_path = os.getenv('DATABASE_URI')
ca_token = os.getenv('CASTING_ASSISTANT_JWT')
cd_token = os.getenv('CASTING_DIRECTOR_JWT')
ep_token = os.getenv('EXECUTIVE_PRODUCER_JWT')

def get_token(role):
    if role == 'asst':
        return {"Authorization": "Bearer {}".format(ca_token)}
    elif role == 'director':
        return {"Authorization": "Bearer {}".format(cd_token)}
    elif role == 'producer':
        return {"Authorization": "Bearer {}".format(ep_token)}


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        #self.testing = True
        self.client = self.app.test_client
        setup_db(self.app, database_path)

        self.ca_token = {"Authorization": "Bearer {}".format(
            os.getenv('CASTING_ASSISTANT_JWT'))}
        self.cd_token = {"Authorization": "Bearer {}".format(
            os.getenv('CASTING_DIRECTOR_JWT'))}
        self.ep_token = {"Authorization": "Bearer {}".format(
            os.getenv('EXECUTIVE_PRODUCER_JWT'))}

        # New Actor for performing test with WRONG DATA ( create, update, get, delete operations )
        self.actor = {
            "name": "Tom Hanks",
            "age": 63,
            "gender": "Male"
        }

        self.actor_for_update = {
            "name": "TOM HANKS"
        }

        # New Movie for performing Test
        self.movie = {
            "title": "Cast Away",
            "release_date": "2000-12-10 12:00:00"
        }

        self.movie_for_update = {
            "title": "CAST AWAY"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    ####
    # Executive Producer for Creating Actor and Movie ( POST )
    ####

    def test_create_actor(self):
        #response = self.client().post('/actors', json=self.actor, headers={ "Authorization": ( ep_token ) })
        response = self.client().post('/actors', headers=get_token('producer'), json=self.actor)
        #body = json.loads(response.data)
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_create_movie(self):
        response = self.client().post('/movies', headers=get_token('producer'), json=self.movie)
        #body = json.loads(response.data)
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)

    ####
    #### Casting Assistant for Viewing Actor and Movie ( GET )
    ####
    def test_get_actors(self):
        response = self.client().get('/actors', headers=get_token('asst'))
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['total_actors'], 1)

    def test_get_movies(self):
        response = self.client().get('/movies', headers=get_token('asst'))
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['total_movies'], 1)

    ####
    #### Casting Director for Updating Actor and Movie ( PATCH )
    ####
    def test_edit_actor(self):
        response = self.client().patch('/actors/1', json=self.actor_for_update, headers=get_token('director'))
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['name'], "TOM HANKS")

    def test_edit_movie(self):
        response = self.client().patch('/movies/1', json=self.movie_for_update, headers=get_token('director'))
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['title'], "CAST AWAY")

    ####
    #### Casting Assistant for Creating Actor and Movie ( RBAC UNAUTHORIZED )
    ####
    def test_create_actor_unauth(self):
        response = self.client().post('/actors', json=self.actor, headers=get_token('asst'))
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(body['code'], "unauthorized")
        self.assertEqual(body['description'], "Permission not found.")

    def test_create_movie_unauth(self):
        response = self.client().post('/movies', json=self.movie, headers=get_token('asst'))
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(body['code'], "unauthorized")
        self.assertEqual(body['description'], "Permission not found.")

    ####
    #### Casting Director for Deleting Movie ( RBAC UNAUTHORIZED )
    ####
    def test_delete_movie_unauth(self):
        response = self.client().delete('/movies/1', headers=get_token('director'))
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(body['code'], "unauthorized")
        self.assertEqual(body['description'], "Permission not found.")

    ####
    #### Executive Producer for Deleting Actor and Movie ( DELETE )
    ####
    def test_delete_actor(self):
        response = self.client().delete('/actors/1', headers=get_token('producer'))
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['deleted'], 1)

    def test_delete_movie(self):
        response = self.client().delete('/movies/1', headers=get_token('producer'))
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['deleted'], 1)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
