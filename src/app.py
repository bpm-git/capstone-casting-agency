#----------------------------------------------------------------------------#
# Import Libraries
#----------------------------------------------------------------------------#
import os
import sys
from dotenv import load_dotenv
from flask import (Flask, request, Response,
                   jsonify, abort)
from flask_cors import CORS
from flask_migrate import Migrate
from auth import (AuthError, requires_auth)
from models import (setup_db, db,
                    Actors, Movies)

# load environment file           
load_dotenv()

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
def create_app(test_config=None):
    '''
    Create app
    '''
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)
    
    CORS(app, resources={'/': {'origins': '*'}})
    
    @app.after_request
    def after_request(response):
        '''
        Use the after_request decorator to set Access-Control-Allow
        '''
        response.headers.add('Access-Control-Allow-Headers',
                                'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                                'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    #----------------------------------------------------------------------------#
    # Controllers.
    #----------------------------------------------------------------------------#
    
    # Actors
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        '''
        Create an endpoint to handle GET requests for actors,
        This endpoint should return a list of actors and
        number of total actors
        '''
        
        # get all actors
        all_actors = Actors.query.order_by(Actors.name).all()
        actors = [actors.format() for actors in all_actors]
    
        # abort if no actors found
        if len(all_actors) == 0:
            abort(404)
        
        # return all actors
        return jsonify({
            'success': True,
            'actors': actors,
            'total_actors': len(all_actors)
        })
    
    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        '''
        Create an endpoint to POST a new actor,
        which will require the name, age and gender
        detals
        '''
    
        # Get the request body
        body = request.get_json()
    
        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')
    
        if ((new_name is None) or (new_age is None) or (new_gender is None)):
            abort(422)
    
        try:
            # create the new actor
            actor = Actors(name=new_name, age=new_age, gender=new_gender)
            actor.insert()
    
            # return the new created actor if successfully created
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
    
        # raise exception for any error during deleting the actor
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(404)
    
    
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(*args, **kwargs):
        id = kwargs['id']
        actor = Actors.query.filter_by(id=id).one_or_none()
    
        if actor is None:
            abort(404)
    
        data = request.get_json()
        new_name = data.get('name', None)
        new_age = data.get('age', None)
        new_gender = data.get('gender', None)
    
        if new_name is not None:
            actor.name = new_name
        
        if new_age is not None:
            actor.age = new_age
        
        if new_gender is not None:
            actor.gender = new_gender
    
        try:
            actor.update()
            
            return jsonify({
                "success": True,
                "actor": actor.format()
            }) 
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(404)
    
    
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(*args, **kwargs):
        '''
        Create an endpoint to DELETE actor using a actor ID.
        '''
        id = kwargs['id']
        actor = Actors.query.filter_by(id=id).one_or_none()
            
        # abort if no actor found
        if actor is None:
            abort(404)
    
        try:
            # delete the actor, when fetched
            actor.delete()
            
            # return true when deleted successfully
            return jsonify({
                'success': True,
                'deleted': id
            })
        
        # raise exception for any error during deleting the actor
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(404)
    
    
    # Movies
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        '''
        Create an endpoint to handle GET requests for movies,
        This endpoint should return a list of movies and
        number of total movies
        '''
        
        # get all movies
        all_movies = Movies.query.order_by(Movies.title).all()
        movies = [movies.format() for movies in all_movies]
    
        # abort if no movies found
        if len(all_movies) == 0:
            abort(404)
        
        # return all movies
        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies': len(all_movies)
        })
    
    
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        '''
        Create an endpoint to POST a new movie,
        which will require the title and
        release date
        '''
    
        # Get the request body
        body = request.get_json()
    
        new_title = body.get('title')
        new_release_date = body.get('release_date')
    
        if ((new_title is None) or (new_release_date is None)):
            abort(422)
    
        try:
            # create the new movie
            movie = Movies(title=new_title, release_date=new_release_date)
            movie.insert()
    
            # return the new created movie if successfully created
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
    
        # raise exception for any error during deleting the movie
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(404)
    
    
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(*args, **kwargs):
        id = kwargs['id']
        movie = Movies.query.filter_by(id=id).one_or_none()
    
        if movie is None:
            abort(404)
    
        data = request.get_json()
        new_title = data.get('title', None)
        new_release_date = data.get('release_date', None)
    
        if new_title is not None:
            movie.title = new_title
        
        if new_release_date is not None:
            movie.recipe = new_release_date
    
        try:
            movie.update()
            
            return jsonify({
                "success": True,
                "movie": movie.format()
            }) 
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(404)
    
    
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(*args, **kwargs):
        '''
        Create an endpoint to DELETE actor using a actor ID.
        '''
        id = kwargs['id']
        movie = Movies.query.filter_by(id=id).one_or_none()
            
        # abort if no movie found
        if movie is None:
            abort(404)
    
        try:
            # delete the movie, when fetched
            movie.delete()
            
            # return true when deleted successfully
            return jsonify({
                'success': True,
                'deleted': id
            })
        
        # raise exception for any error during deleting the movie
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(404)
    
    
    #----------------------------------------------------------------------------#
    # Error Handling
    #----------------------------------------------------------------------------#
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    
    '''
    implement error handler for AuthError
        error handler should conform to general task above 
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        response = jsonify(e.error)
        response.status_code = e.status_code
        return response
    
    return app

app = create_app()

#----------------------------------------------------------------------------#
# Run
#----------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
