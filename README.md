# Installation

Copy `.env.example` to `.env` and fill variables

## Manual

1. Create database:
    ```sql
    # create user tarly with password 'tarly';
    # create database tarly owner tarly;
    ```
    or 
    ```bash
    createuser tarly -P
    createdb tarly -O tarly
    ```
1. Initial dependencies: 
    ```bash
    $ poetry install
    ```
1. Migrate database and create superuser:
    ```bash
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    ```
1. To seed database with random data
    ```bash
       ./manage.py populate_db
    ```

## via docker-compose:

1. Build:
    ```bash
    $ docker-compose build
    ```
1. Start:
    ```bash
    $ docker-compose up -d
    ```
1. Run management command like:
    ```bash
    $ docker exec -it tarly_web_1 /bin/sh
    /code # ./manage.py createsuperuser
    ```

## Usage

open http://localhost:8000 to view api documentation and use endpoints  

## Test  
```bash
     # ./manage.py test
```

       
