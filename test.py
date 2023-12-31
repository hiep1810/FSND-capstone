import unittest
import json
import os
from api import app
from  database.models import Actor, Movie, setup_db


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.casting_assistant_token = os.environ['CASTING_ASSISTANT_TOKEN']
        self.casting_director_token = os.environ['CASTING_DIRECTOR_TOKEN']
        self.executive_producer_token = os.environ['EXECUTIVE_PRODUCER_TOKEN']
        self.app = app
        self.client = self.app.test_client
        
        # binds the app to the current context
        with self.app.app_context():

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
        pass


    def test_authorization_header_missing(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"]["code"], "authorization_header_missing")
        self.assertEqual(data["message"]["description"], "Authorization header is expected.")

    # Tests for GET /actors
    def test_get_actors_success(self):
        response = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(data['actors']), 0)

    def test_get_actors_failure(self):
        response = self.client().get('/actors/invalid')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for GET /movies
    def test_get_movies_success(self):
        response = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(data['movies']), 0)

    def test_get_movies_failure(self):
        response = self.client().get('/movies/invalid')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for GET /actors/<id>
    def test_get_actor_by_id(self):
        with self.app.app_context():
            actor = Actor(name='John Doe', age=30, gender='Male')
            actor.insert()


            response = self.client().get(f'/actors/{actor.id}', headers={
                'Authorization': "Bearer {}".format(self.casting_assistant_token)
            })
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['actors'][0]['name'], 'John Doe')
            self.assertEqual(data['actors'][0]['age'], 30)
            self.assertEqual(data['actors'][0]['gender'], 'Male')

    def test_get_actor_by_id_failure(self):
        response = self.client().get('/actors/invalid')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Tests for GET /movies/<id>
    def test_get_movie_by_id(self):
        with self.app.app_context():
            movie = Movie(title='Example Movie', release_date='2022-10-18')
            movie.insert()

            response = self.client().get(f'/movies/{movie.id}', headers={
                'Authorization': "Bearer {}".format(self.casting_assistant_token)
            })
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['movies'][0]['title'], 'Example Movie')
            self.assertEqual(data['movies'][0]['release_date'], '2022-10-18')

    def test_get_movie_by_id_failure(self):
        response = self.client().get('/movies/invalid')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Tests for POST /actors
    def test_create_actor_success(self):
        actor = {'name': 'Brad Pitt', 'age': 59, 'gender': 'Male'}

        response = self.client().post('/actors', json=actor, headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'][0]['name'], 'Brad Pitt')
        self.assertEqual(data['actors'][0]['age'], 59)
        self.assertEqual(data['actors'][0]['gender'], 'Male')

    def test_create_actor_failure(self):
        response = self.client().post('/actors', json={}, headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Tests for POST /movies
    def test_create_movie_success(self):
        movie = {'title': 'Fight Club', 'release_date': '1999-10-15'}
        response = self.client().post('/movies', json=movie, headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        })
        data = json.loads(response.data)


        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'][0]['title'], 'Fight Club')
        self.assertEqual(data['movies'][0]['release_date'], '1999-10-15')

    def test_create_movie_failure(self):
        response = self.client().post('/movies', json={}, headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Tests for PATCH /actors/<id>
    def test_update_actor_success(self):
        actor = {'name': 'Updated Name'}
        response = self.client().patch(f'/actors/{self.actor_id}', json=actor, headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'][0]['name'], 'Updated Name')

    def test_update_actor_failure(self):
        response = self.client().patch('/actors/500', json={}, headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for PATCH /movies/<id>
    def test_update_movie_success(self):
        movie = {'title': 'Updated Title'}
        response = self.client().patch(f'/movies/{self.movie_id}', json=movie, headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'][0]['title'], 'Updated Title')

    def test_update_movie_failure(self):
        response = self.client().patch('/movies/500', json={}, headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for DELETE /actors/<id>
    def test_delete_actor_success(self):
        response = self.client().delete(f'/actors/{self.actor_id}', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], self.actor_id)

    def test_delete_actor_failure(self):
        response = self.client().delete('/actors/500', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Tests for DELETE /movies/<id>
    def test_delete_movie_success(self):
        response = self.client().delete(f'/movies/{self.movie_id}', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], self.movie_id)

    def test_delete_movie_failure(self):
        response = self.client().delete('/movies/500', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

if __name__ == '__main__':
    unittest.main()