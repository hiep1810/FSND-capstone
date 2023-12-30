import os
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

# Replace the values with your actual database information
username = os.environ['DATABASE_USERNAME']
password = os.environ['DATABASE_PASSWORD']
host = os.environ['DATABASE_HOST']
port = os.environ['DATABASE_PORT']
database_name = os.environ['DATABASE_NAME']

# Construct the URI
database_path = f'postgresql://{username}:{quote_plus(password)}@{host}:{port}/{database_name}'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test

    # Create actors
    actor1 = Actor(name='Actor 1', age=30, gender='Male')
    actor2 = Actor(name='Actor 2', age=25, gender='Female')
    actor3 = Actor(name='Actor 3', age=35, gender='Male')
    db.session.add_all([actor1, actor2, actor3])
    db.session.commit()

    # Create movies
    movie1 = Movie(title='Movie 1', release_date=date(2022, 1, 1))
    movie2 = Movie(title='Movie 2', release_date=date(2023, 2, 15))
    movie3 = Movie(title='Movie 3', release_date=date(2024, 5, 10))
    db.session.add_all([movie1, movie2, movie3])
    db.session.commit()

    # Associate actors with movies
    movie1.actors.extend([actor1, actor2])
    movie2.actors.extend([actor2, actor3])
    movie3.actors.append(actor3)
    db.session.commit()


# Association table for the many-to-many relationship between actors and movies
ActorMovie = db.Table('ActorMovie',
    db.Column('actor_id', db.Integer, db.ForeignKey('Actor.id', ondelete='CASCADE'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id', ondelete='CASCADE'), primary_key=True)
)

class BaseModel(db.Model):
    __abstract__ = True

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Movie 1'
            movie.update()
    '''
    def update(self):
        db.session.commit()

'''
Movie
a persistent Movie entity, extends the base SQLAlchemy Model
'''
class Movie(BaseModel):
    __tablename__ = 'Movie'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # String Title
    title = db.Column(db.String(128), nullable=False)
    # Release Date
    release_date = db.Column(db.Date, nullable=False)
    # Define the relationship with the Actor table through the ActorMovie table 
    actors = db.relationship('Actor', \
                             secondary=ActorMovie, \
                             backref='movies')


    # Define the string representation of a Movie object
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%Y-%m-%d'),
            'actors': [actor.serialize() for actor in self.actors]
        }

'''
Actor
a persistent Actor entity, extends the base SQLAlchemy Model
'''
class Actor(BaseModel):
    __tablename__ = 'Actor'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(16), nullable=False)

    # Define the string representation of a Actor object
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
