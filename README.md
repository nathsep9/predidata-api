# Predidata-API

This repo is functionality complete — PR's and issues welcome!

## Installation

1. Clone this repository: `git clone git@github.com:nathsep9/predidata-api.git`.
2. `cd` into `predidata-api`: `cd predidata-api`
3. Install dependencies:

   pip install -r requirements.txt

## Migrations

flask db upgrade

## Running

flask run

## Docker

configure the environment file as follows:

```
DB_DRIVER = 'postgresql'
DB_HOST='db'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_NAME='predidata'

DB_PORT=5435
```

the image is raised with the following command:

```
docker-compose up
```
