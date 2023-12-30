from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import os
from  database.models import db_drop_and_create_all, setup_db, Actor, Movie

from auth.auth import AuthError, requires_auth


QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', '1')
    setup_db(app)
    """
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
                    'Allow-Control-Allow-Headers',
                    'Content-Type,Authorization,true'
                    )
        response.headers.add(
                    'Allow-Control-Allow-Methods',
                    'GET, POST, PATCH, DELETE, OPTIONS'
                    )
        return response

    with app.app_context():
        db_drop_and_create_all()
        '''
            GET /
        '''
        @app.route('/', methods=['GET'])
        def hello_world():
            return jsonify({
                'success': True,
                'message': 'hello world~!!'
            }), 200

        '''
            GET /actors
        '''
        @app.route('/actors', methods=['GET'])
        @requires_auth('get:actors')
        def get_actors(payload):
        
            page = request.args.get('page',1,type=int)

            if page < 1:
                abort(422)
                
            try:
                start = (page - 1) * QUESTIONS_PER_PAGE
                end = start + QUESTIONS_PER_PAGE

                actors = Actor.query.all()
                return jsonify({
                    'success': True,
                    'actors': [actor.serialize() for actor in actors][start:end]
                }), 200
            except Exception as e:
                print(e)
                abort(500)

        '''
            GET /actors/<id>
        '''
        @app.route('/actors/<int:actor_id>', methods=['GET'])
        @requires_auth('get:actors')
        def get_actor(payload, actor_id):
            try:
                actor = Actor.query.get(actor_id)

                if actor is None:
                    abort(404)

                return jsonify({
                    'success': True,
                    'actors': [actor.serialize()]
                }), 200
            except Exception as e:
                print(e)
                abort(500)

        '''
            GET /movies
        '''
        @app.route('/movies', methods=['GET'])
        @requires_auth('get:movies')
        def get_movies(payload):
            try:
                movies = Movie.query.all()
                return jsonify({
                    'success': True,
                    'movies': [movie.serialize() for movie in movies]
                }), 200
            except Exception as e:
                print(e)
                abort(500)

        '''
            GET /movies/<id>
        '''
        @app.route('/movies/<int:movie_id>', methods=['GET'])
        @requires_auth('get:movies')
        def get_movie(payload, movie_id):
            try:
                movie = Movie.query.get(movie_id)

                if movie is None:
                    abort(404)

                return jsonify({
                    'success': True,
                    'movies': [movie.serialize()]
                }), 200
            except Exception as e:
                print(e)
                abort(500)

        '''
            POST /actors
        '''
        @app.route('/actors', methods=['POST'])
        @requires_auth('post:actors')
        def create_actor(payload):
            body = request.get_json()
            req_name = body.get('name', None)
            req_age = body.get('age', None)
            req_gender = body.get('gender', None)

            if not req_name \
            or not req_age \
            or not req_gender:
                abort(422)

            try:
                actor = Actor(name=req_name, age=req_age, gender=req_gender)
                actor.insert()
                return jsonify({
                    'success': True,
                    'actors': [actor.serialize()]
                }), 200
            except Exception as e:
                print(e)
                abort(500)

        '''
            POST /movies
        '''
        @app.route('/movies', methods=['POST'])
        @requires_auth('post:movies')
        def create_movie(payload):
            body = request.get_json()
            req_title = body.get('title', None)
            req_release_date = body.get('release_date', None)
            req_actors = body.get('actors', None)

            if not req_title \
            or not req_release_date:
                abort(422)

            try:
                # Create the movie
                movie = Movie(title=req_title, release_date=req_release_date)

                # Associate actors with the movie
                if  req_actors is not None:
                    if isinstance(req_actors, list):
                        actors = []
                        for actor_id in req_actors:
                            actor = Actor.query.get(actor_id)
                            if actor:
                                movie.actors.append(actor)
                                actors.append(actor)
                    else:
                        abort(422)

                movie.insert()

                return jsonify({
                    'success': True,
                    'movies': [movie.serialize()]
                }), 200
            except Exception as e:
                print(e)
                abort(500)
                
        '''
            PATCH /actors/<id>
        '''
        @app.route('/actors/<int:actor_id>', methods=['PATCH'])
        @requires_auth('patch:actors')
        def update_actor(payload, actor_id):
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)

            body = request.get_json()
            req_name = body.get('name', None)
            req_age = body.get('age', None)
            req_gender = body.get('gender', None)

            try:
                if req_name  is not None:
                    actor.name = req_name
                if req_age  is not None:
                    actor.age = req_age
                if req_gender  is not None:
                    actor.gender = req_gender

                actor.update()
                return jsonify({
                    'success': True,
                    'actors': [actor.serialize()]
                }), 200
            except Exception as e:
                print(e)
                abort(500)

        '''
            PATCH /actors/<id>
        '''
        @app.route('/movies/<int:movie_id>', methods=['PATCH'])
        @requires_auth('patch:movies')
        def update_movie(payload, movie_id):
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)

            body = request.get_json()
            req_title = body.get('title', None)
            req_release_date = body.get('release_date', None)
            req_actor_ids = body.get('actor_ids', [])

            try:
                if req_title  is not None:
                    movie.title = req_title
                if req_release_date  is not None:
                    movie.release_date = req_release_date

                # Retrieve the actors and update the movie's actor relationships
                actors = Actor.query.filter(Actor.id.in_(req_actor_ids)).all()
                movie.actors = actors

                movie.update()

                return jsonify({
                    'success': True,
                    'movies': [movie.serialize()]
                }), 200
            except Exception as e:
                print(e)
                abort(500)
        '''
            DELETE /actors/<id>
        '''
        @app.route('/actors/<int:actor_id>', methods=['DELETE'])
        @requires_auth('delete:actors')
        def delete_actor(payload, actor_id):
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)
            try:
                actor.delete()

                return jsonify({
                    'success': True,
                    'delete': actor_id
                }), 200
            except Exception as e:
                print(e)
                abort(500)

        '''
            DELETE /movies/<id>
        '''
        @app.route('/movies/<int:movie_id>', methods=['DELETE'])
        @requires_auth('delete:movies')
        def delete_movie(payload, movie_id):
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)
            try:
                movie.delete()

                return jsonify({
                    'success': True,
                    'delete': movie_id
                }), 200
            except Exception:
                abort(500)

    ###########################################################################
        '''
            Error Handling
        '''
        @app.errorhandler(422)
        def unprocessable(error):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422


        @app.errorhandler(404)
        def not_found(error):
            return jsonify({
                'success': False,
                'error': 404,
                'message': 'Resource not found'
            }), 404



        @app.errorhandler(AuthError)
        def handle_auth_error(error):
            return jsonify({
                'success': False,
                'error': error.status_code,
                'message': error.error
            }), error.status_code
        
        return app