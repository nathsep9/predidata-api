from blueprints import properties
from models.Owner import Owner, owner_schema, owners_schema
from models import Property, properties_schema
from database import getSession
from flask import jsonify, request
from flask.blueprints import Blueprint


ownersBp = Blueprint('owners', __name__)


@ownersBp.route("/owners", methods=['POST'])
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


@ownersBp.route("/owners", methods=['GET'])
def get_owners():
    session = getSession()

    owners = session.query(Owner).all()

    return jsonify(owners_schema.dump(owners))


@ownersBp.route("/owners/<int:owner_id>", methods=['DELETE'])
def delete_owner(owner_id):
    session = getSession()

    owner = session.query(Owner).get(owner_id)

    session.delete(owner)
    session.commit()

    return jsonify({
        'message': 'Owner deleted'
    })


@ownersBp.route("/owners/<int:owner_id>", methods=['GET'])
def get_owner(owner_id):
    session = getSession()

    owner = session.query(Owner).get(owner_id)
    if owner is None:
        return jsonify({
            'message': 'Owner not found'
        }), 404

    return jsonify(owner_schema.dump(owner))


@ownersBp.route("/owners/<int:owner_id>/properties", methods=['GET'])
def get_owner_properties(owner_id):
    session = getSession()

    owner = session.query(Owner).get(owner_id)
    if owner is None:
        return jsonify({
            'message': 'Owner not found'
        }), 404

    properties = owner.properties

    return jsonify(properties_schema.dump(properties))


@ownersBp.route("/owners/<int:owner_id>/properties/<int:property_id>", methods=['DELETE'])
def delete_owner_property(owner_id, property_id):
    session = getSession()

    owner = session.query(Owner).get(owner_id)
    if owner is None:
        return jsonify({
            'message': 'Owner not found'
        }), 404

    property = session.query(Property).get(property_id)
    if property is None:
        return jsonify({
            'message': 'Property not found'
        }), 404

    owner.properties.remove(property)
    session.commit()

    return jsonify({
        'message': 'Property deleted'
    })


@ownersBp.route("/owners/<int:owner_id>/properties", methods=['POST'])
def add_owner_property(owner_id):
    session = getSession()

    request_data = request.get_json()

    owner = session.query(Owner).get(owner_id)
    if owner is None:
        return jsonify({
            'message': 'Owner not found'
        }), 404

    properties_data = request_data['properties']
    properties = session.query(Property).filter(
        Property.id.in_(properties_data)).all()
    owner.properties.extend(properties)
    session.commit()
    return jsonify(properties_schema.dump(properties))

# get available properties


@ownersBp.route("/owners/<int:owner_id>/properties/available", methods=['GET'])
def get_available_properties(owner_id):
    session = getSession()

    owner = session.query(Owner).get(owner_id)
    if owner is None:
        return jsonify({
            'message': 'Owner not found'
        }), 404

    ids = owner.properties.all()
    ids = [i.id for i in ids]
    properties = session.query(Property).filter(
        Property.id.notin_(ids)
    ).all()

    return jsonify(properties_schema.dump(properties))
