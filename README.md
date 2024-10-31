# Hagan Realty monolith app 

## Description



## Architecture

Project is designed as a Django-admin application for Hagan Realty internal usage.
It uses PostgreSQL as a database

## Pre-requirements

You need to have installed Docker and Docker-compose on your machine.

Also you need to have pre paid BrightMLS API account


# Local development

## Installation

Local development is done with docker-compose.
1. Clone the repository
2. Copy .env.example to .env and fill in the variables (Request secrets from your lead developer)
4. Run `docker-compose up -d --build` (for pycharm users: you can use docker-compose.yml as a remote interpreter)
5. Run `docker-compose exec web python manage.py migrate` (for pycharm users: you can run `python manage.py migrate` from pycharm services > docker-compose > web > terminal)
6. To access adminpanel, run `docker-compose exec ft_web python manage.py createsuperuser` (for pycharm users: you can run `python manage.py createsuperuser` from pycharm services > docker-compose > web > terminal)
7. Open http://localhost:8000 in your browser

## Logs

To see logs of the project, run `docker-compose logs -f` in the root of the project
       

## Database

In db container:
`pg_dump --username=local_dbuser --host=localhost local_db > 2024-10-29.sql`
