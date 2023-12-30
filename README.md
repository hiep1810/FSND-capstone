# FSND capstone Details

-----
Heroku Link: https://ry-fsnd-capstone.herokuapp.com

While running locally: http://localhost:5000
## Introduction

### Overview

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

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
- Tests:
    - One test for success behavior of each endpoint
    - One test for error behavior of each endpoint
    - At least two tests of RBAC for each role

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework

## Development Setup

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

