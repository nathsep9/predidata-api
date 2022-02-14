
from models.Owner import Owner, owner_schema, owners_schema
from models.Property import Property, property_schema, properties_schema
from database import getSession
from flask import jsonify, request
from flask.blueprints import Blueprint


propertiesBp = Blueprint('properties', __name__)


@propertiesBp.route("/properties", methods=['POST'])
def create_property():
    session = getSession()

    request_data = request.get_json()

    property = Property(
        name=request_data['name'],
        address=request_data['address'],
        real_estate_registration=request_data['real_estate_registration'],
        type_property=request_data['type_property']
    )

    session.add(property)
    session.commit()

    owners_array = request_data['owners']

    owners = session.query(Owner).filter(Owner.id.in_(owners_array)).all()
    property.owners = owners
    session.commit()

    return jsonify(property_schema.dump(property))


@propertiesBp.route("/properties", methods=['GET'])
def get_properties():
    session = getSession()

    properties = session.query(Property).all()

    return jsonify(properties_schema.dump(properties))


@propertiesBp.route("/properties/<int:property_id>", methods=['DELETE'])
def delete_property(property_id):
    session = getSession()

    property = session.query(Property).get(property_id)

    session.delete(property)
    session.commit()

    return jsonify({
        'message': 'Property deleted'
    })


@propertiesBp.route("/properties/<int:property_id>", methods=['GET'])
def get_property(property_id):
    session = getSession()

    property = session.query(Property).get(property_id)
    if property is None:
        return jsonify({
            'message': 'Property not found'
        }), 404

    return jsonify(property_schema.dump(property))


@propertiesBp.route("/properties/<int:property_id>/owners", methods=['GET'])
def get_property_owners(property_id):
    session = getSession()

    property = session.query(Property).get(property_id)
    if property is None:
        return jsonify({
            'message': 'Property not found'
        }), 404

    owners = property.owners

    return jsonify(owners_schema.dump(owners))


@propertiesBp.route("/properties/<int:property_id>/owners/<int:owner_id>", methods=['DELETE'])
def delete_property_owner(property_id, owner_id):
    session = getSession()

    property = session.query(Property).get(property_id)
    if property is None:
        return jsonify({
            'message': 'Property not found'
        }), 404

    owner = session.query(Owner).get(owner_id)
    if owner is None:
        return jsonify({
            'message': 'Owner not found'
        }), 404

    property.owners.remove(owner)
    session.commit()

    return jsonify({
        'message': 'Owner deleted'
    })


@propertiesBp.route("/properties/<int:property_id>/owners/available", methods=['GET'])
def get_property_available_owners(property_id):
    session = getSession()

    property = session.query(Property).get(property_id)
    if property is None:
        return jsonify({
            'message': 'Property not found'
        }), 404

    ids = [owner.id for owner in property.owners]

    owners = session.query(Owner).filter(Owner.id.notin_(ids)).all()

    return jsonify(owners_schema.dump(owners))


@propertiesBp.route("/properties/<int:property_id>/owners", methods=['POST'])
def add_property_owner(property_id):
    session = getSession()

    request_data = request.get_json()

    property = session.query(Property).get(property_id)
    if property is None:
        return jsonify({
            'message': 'Property not found'
        }), 404

    owners_data = request_data['owners']

    owners = session.query(Owner).filter(Owner.id.in_(owners_data)).all()
    property.owners.extend(owners)
    session.commit()

    return jsonify(owners_schema.dump(owners))
