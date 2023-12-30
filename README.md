# FSND capstone Details

-----
Render Link: https://filmography.onrender.com/
While running locally: http://localhost:5000

## Introduction

### Project Motivation



The motivation for creating The Casting Agency application is to simplify the movie production process. The application automates tasks, centralizes information, and improves communication. It also allows for data analysis to make better casting decisions. The goal is to simplify casting, increase productivity, and choose the right actors for each role.



### Roles
- Models:
    - Movies with attributes title and release date
    - Actors with attributes name, age and gender
- Endpoints:
    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/
- Roles:
    - Casting Assistant
        - Can view actors and movies
    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database


## Tech Stack (Dependencies)

**Flask** is a lightweight backend microservices framework. Flask is required to handle requests and responses.

**SQLAlchemy** is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

**Flask-CORS** is the extension we'll use to handle cross origin requests from our frontend server.

**Auth0** is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

**PostgreSQL** this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.


## Running Locally

1. **Install the dependencies:**
```
pip install -r requirements.txt
```

2. **Database:**

Log in to an interactive Postgres session using the following command:

```
sudo -iu postgres psql
```
First, create a database for your project:
```
CREATE DATABASE filmography;
```
Next, create a database user for our project. Make sure to select a secure password:
```
CREATE USER admin WITH PASSWORD 'admin';
```

3. **Run the development server:**

Each time you open a new terminal session, run:

```
#DATABASE
export DATABASE_USERNAME='admin'
export DATABASE_PASSWORD='admin'
export DATABASE_HOST='localhost'
export DATABASE_PORT=5432
export DATABASE_NAME='filmography'

export FLASK_APP=api.py;
export FLASK_DEBUG='1'

export UTH0_DOMAIN='your_auth0_domain'
export API_AUDIENCE='auth0_audience'
```

-----
# Flask API Documentation

Introduction
This document provides detailed information about the endpoints available in the Flask API code provided. The API allows users to perform CRUD operations on actors and movies in a database.

## Table of Contents
Hello World
Get Actors
Get Actor
Get Movies
Get Movie
Create Actor
Create Movie
Update Actor
Update Movie
Delete Actor
Delete Movie

### GET /

- Returns a simple hello world message
- Does not require authentication

**Example Response**

```json
{
  "message": "hello world~!!", 
  "success": true
}
```

### GET /actors
```md  
# GET /actors
```

- Returns paginated actors from the database
- Requires `get:actors` permission
- Accepts `page` parameter to specify page number, defaults to 1

**Example Response**

```json
{
  "actors": [
    {
      "age": 45, 
      "gender": "male",
      "id": 1,
      "name": "Tom Cruise"
    }
  ],
  "success": true
}
```


### GET /actors/<id>
```md
# GET /actors/<id>
```

- Returns actor with specified ID
- Requires `get:actors` permission

**Example Response**

```json
{
  "actors": [
    {
      "age": 45,
      "gender": "male", 
      "id": 1,
      "name": "Tom Cruise"
    }
  ],
  "success": true
}
```

### GET /movies
```md
# GET /movies
```

- Returns all movies
- Requires `get:movies` permission

**Example Response** 

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "2022-01-01",  
      "title": "Top Gun: Maverick" 
    }
  ],
  "success": true
}
```


### GET /movies/<id>
```md
# GET /movies/<id>
```

- Returns movie with specified ID
- Requires `get:movies` permission

**Example Response**

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "2022-01-01",
      "title": "Top Gun: Maverick"
    }
  ],
  "success": true  
}
```


### POST /actors
```md
# POST /actors
```

- Creates a new actor
- Requires `post:actors` permission
- Request body must contain `name`, `age` and `gender`

**Example Request**

```json
{
  "name": "Tom Cruise",
  "age": 45,
  "gender": "male"
}
```

**Example Response**
```json
{
  "actors": [
    {
      "age": 45,
      "gender": "male",
      "id": 1,
      "name": "Tom Cruise"   
    }
  ],
  "success": true
}
```

### POST /movies
```md
# POST /movies
```

- Creates a new movie
- Requires `post:movies` permission
- Request body must contain `title` and `release_date`
- Can optionally contain list of `actors` to associate with the movie

**Example Request**

```json
{
  "title": "Top Gun: Maverick",
  "release_date": "2022-05-27",
  "actors": [1, 2] 
}
```
**Example Response**
```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "2022-05-27",
      "title": "Top Gun: Maverick"  
    }
  ],
  "success": true
}
```


### PATCH /actors/<id>
```md  
# PATCH /actors/<id>
```

- Updates an existing actor
- Requires `patch:actors` permission
- Can update `name`, `age` or `gender`

**Example Request**

```json
{
  "name": "Tom Cruise" 
}
```
**Example Response**
```json
{
  "actors": [
    {
      "age": 45,  
      "gender": "male",
      "id": 1,
      "name": "Tom Cruise"
    }
  ],
  "success": true
}
```


### PATCH /movies/<id> 
```md
# PATCH /movies/<id>
```

- Updates an existing movie
- Requires `patch:movies` permission  
- Can update `title` or `release_date`
- Can update list of actor IDs associated with the movie

**Example Request**

```json
{
  "title": "Top Gun 2",
  "actor_ids": [1, 2, 3] 
}
```

**Example Response**
```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "2022-05-27",
      "title": "Top Gun 2"
    }
  ],
  "success": true
}
```


### DELETE /actors/<id>
```md
# DELETE /actors/<id>
```

- Deletes an actor with specified ID 
- Requires `delete:actors` permission

**Example Response**

```json
{
  "delete": 1,
  "success": true
}


### DELETE /movies/<id>
```md  
# DELETE /movies/<id>
```

- Deletes movie with specified ID
- Requires `delete:movies` permission

**Example Response**

```json
{
  "delete": 1,
  "success": true
}
```