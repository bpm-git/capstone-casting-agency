Capstone Casting Agency
-----

### Introduction

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

### Overview

This app provides a platform to Castng Assistants, Casting Directors and Executive Producers in managing a directory of movies and actors.

### Tech Stack

Our tech stack will include:

* **Python3** and **Flask** as our server language and server framework
* **PostgreSQL** as our database of choice
* **SQLAlchemy ORM** to be our ORM library of choice
* **Flask** lighweight backend microservices framework and is required to handle requests and responses.
* **Flask-CORS** extension to handle cross origin request
* **Flask-Migrate** for creating and running schema migrations
* **Auth0** for authentication
* **jose** JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.
* **Heroku** for deployment of the application


### Main Files: Project Structure

  ```sh
    ├── src                   ('All the backend api part are structured under this directory')
    │   │
    │   ├── app.py            ('App file to process the routes, manages the data model based upon auth')  
    │   ├── auth.py           ('Authentication and Authorization')
    │   ├── models.py         ('Has all the data model files and CRUD performer')
    │   │── requirements.txt  ('has all the dependent packges required for running the application')
    │   │── tests.py          ('Performing all the tests for the applications')
    │
    ├── README.md
  
  ```

### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=app
  $ export FLASK_ENV=development # enables debug mode
  $ flask run --reload
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)


### API End Point 

POST '/actors'

* This will create new actors
* Parameter: None
* Request:
```
{
    "name": "Tom Hanks",
    "age": 63,
    "gender": "Male"
}
```
* Response
```
{
    "actor": {
        "age": 63,
        "gender": "Male",
        "id": 1,
        "name": "Tom Hanks"
    },
    "success": true
}
```

POST '/movies'

* This will create new movies
* Parameter: None
* Request:
```
{
    "title": "Cast Away",
    "release_date": "2000-12-10 12:00:00"
}
```
* Response
```
{
    "movie": {
        "id": 1,
        "release_date": "Sun, 10 Dec 2000 12:00:00 GMT",
        "title": "Cast Away"
    },
    "success": true
}
```

GET '/actors'

* This will list all the actors
* Parameter: None
* Response
```
{
    "actors": [
        {
            "age": 63,
            "gender": "Male",
            "id": 1,
            "name": "Tom Hanks"
        }
    ],
    "success": true,
    "total_actors": 1
}
```

GET '/movies'

* This will list all the movies
* Parameter: None
* Response
```
  {
    "movies": [
        {
            "id": 1,
            "release_date": "Sun, 10 Dec 2000 12:00:00 GMT",
            "title": "Cast Away"
        }
    ],
    "success": true,
    "total_movies": 1
}
```

PATCH '/actors/<actor_id>'
* This will update actor for a given id
* Parameter: actor_id
* Request
```
{
    "name": "TOM HANKS"
}
```
* Response
```
{
  "actor": {
      "age": 63,
      "gender": "Male",
      "id": 1,
      "name": "TOM HANKS"
  },
  "success": true
}
```

PATCH '/movies/<movie_id>'
* This will update movie for a given id
* Parameter: movie_id
* Request
```
{
    "title": "CAST AWAY"
}
```
* Response
```
{
  "movie": {
      "id": 1,
      "release_date": "Sun, 10 Dec 2000 12:00:00 GMT",
      "title": "CAST AWAY"
  },
  "success": true
}
```
DELETE '/actors/<actor_id>'

* This will delete actor for a given id
* Parameter: actor_id
* Response
```
{
    "deleted": 1,
    "success": true
}
```
DELETE '/movies/<movie_id>'

* This will delete actor for a given id
* Parameter: actor_id
* Response
```
{
    "deleted": 1,
    "success": true
}
```

UnAuthorized Response

```
{
    "code": "unauthorized",
    "description": "Permission not found."
}
```

### Testing

To run the tests, run
```
dropdb capstone_test
createdb capstone_test
python tests.py
```
