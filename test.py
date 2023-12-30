import unittest
import json
import os
from api import create_app, setup_db
from  database.models import Actor, Movie


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.user_token = os.environ['CASTING_ASSISTANT_TOKEN']
        self.manager_token = os.environ['CASTING_DIRECTOR_TOKEN']
        self.admin_token = os.environ['CASTING_DIRECTOR_TOKEN']
        self.app = create_app()
        self.client = self.app.test_client
        self.db = setup_db(self.app)

        # Sample data
        self.sample_actor = {'name': 'Tom Cruise', 'age': 59, 'gender': 'M'}
        self.sample_movie = {'title': 'Mission Impossible', 'release_date': '1996-05-22'}

        actor = Actor(**self.sample_actor)
        actor.insert()
        movie = Movie(**self.sample_movie)
        movie.insert()

        self.actor_id = actor.id
        self.movie_id = movie.id

    def tearDown(self):
        self.session.remove()
        self.drop_all()
        pass

    # Tests for GET /actors
    def test_get_actors_success(self):
        response = self.app.get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(data['actors']), 0)

    def test_get_actors_failure(self):
        response = self.app.get('/actors/invalid')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for GET /movies
    def test_get_movies_success(self):
        response = self.app.get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(data['movies']), 0)

    def test_get_movies_failure(self):
        response = self.app.get('/movies/invalid')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for GET /actors/<id>
    def test_get_actor_by_id(self):
        actor = Actor(name='John Doe', age=30)
        actor.insert()

        response = self.app.get(f'/actors/{self.actor_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'John Doe')
        self.assertEqual(data['actor']['age'], 30)

    def test_get_actor_by_id_failure(self):
        response = self.app.get('/actors/invalid')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Tests for GET /movies/<id>
    def test_get_movie_by_id(self):
        movie = Movie(title='Example Movie', year=2022)
        movie.insert()

        response = self.app.get('/movies/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'Example Movie')
        self.assertEqual(data['movie']['year'], 2022)

    def test_get_movie_by_id_failure(self):
        response = self.app.get('/movies/invalid')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Tests for POST /actors
    def test_create_actor_success(self):
        actor = {'name': 'Brad Pitt', 'age': 59, 'gender': 'M'}
        response = self.app.post('/actors', json=actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'][0]['name'], 'Brad Pitt')

    def test_create_actor_failure(self):
        response = self.app.post('/actors', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Tests for POST /movies
    def test_create_movie_success(self):
        movie = {'title': 'Fight Club', 'release_date': '1999-10-15'}
        response = self.app.post('/movies', json=movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'][0]['title'], 'Fight Club')

    def test_create_movie_failure(self):
        response = self.app.post('/movies', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Tests for PATCH /actors/<id>
    def test_update_actor_success(self):
        actor = {'name': 'Updated Name'}
        response = self.app.patch(f'/actors/{self.actor_id}', json=actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'][0]['name'], 'Updated Name')

    def test_update_actor_failure(self):
        response = self.app.patch('/actors/500', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for PATCH /movies/<id>
    def test_update_movie_success(self):
        movie = {'title': 'Updated Title'}
        response = self.app.patch(f'/movies/{self.movie_id}', json=movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'][0]['title'], 'Updated Title')

    def test_update_movie_failure(self):
        response = self.app.patch('/movies/500', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for DELETE /actors/<id>
    def test_delete_actor_success(self):
        response = self.app.delete(f'/actors/{self.actor_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], self.actor_id)

    def test_delete_actor_failure(self):
        response = self.app.delete('/actors/500')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for DELETE /movies/<id>
    def test_delete_movie_success(self):
        response = self.app.delete(f'/movies/{self.movie_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], self.movie_id)

    def test_delete_movie_failure(self):
        response = self.app.delete('/movies/500')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

if __name__ == '__main__':
    unittest.main()