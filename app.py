import os
from flask import Flask, jsonify, request

from database import db, getSession, migrate
from ma import ma

import models
from models.Owner import Owner, owner_schema

from models.Property import Property, property_schema

app = Flask(__name__)


def shell_context_processor():
    return dict(db=db, models=models, **models.__dict__)


app.shell_context_processor(shell_context_processor)

uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'development' == app.env
app.secret_key = os.getenv('SECRET_KEY')

# Cors


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    return response


db.init_app(app)
migrate.init_app(app)
ma.init_app(app)


@app.route("/")
def main():
    return "<p>PrediData API!</p>"


@app.route("/db")
def db_test():
    session = getSession()
    return str(session.execute('SELECT 1+1').scalar())


@app.route("/owner", methods=['POST'])
def create_owner():
    session = getSession()

    request_data = request.get_json()

    owner = Owner(
        name=request_data['name'],
        document=request_data['document'],
        type_document=request_data['type_document']
    )

    session.add(owner)
    session.commit()

    return jsonify(owner_schema.dump(owner))


@app.route("/owner/<int:owner_id>", methods=['GET'])
def get_owner(owner_id):
    session = getSession()

    owner = session.query(Owner).get(owner_id)

    return jsonify(owner_schema.dump(owner))


@app.route("/property/<int:property_id>", methods=['GET'])
def get_property(property_id):
    session = getSession()

    property = session.query(Property).get(property_id)

    return jsonify(property_schema.dump(property))
