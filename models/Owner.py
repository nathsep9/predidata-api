import enum
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from database import db
from ma import ma


class TypeDocument(enum.IntEnum):
    TI = 1
    CC = 2
    CE = 3
    NIT = 4


owners_properties = db.Table(
    'owners_properties',
    db.Column('owner_id', db.Integer, db.ForeignKey('owners.id')),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'))
)


class Owner(db.Model):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    document = Column(BigInteger, unique=True, nullable=False)
    type_document = Column(Integer, nullable=False)
    properties = relationship(
        'Property', secondary=owners_properties, backref='owners', lazy='dynamic'
    )

    def __repr__(self):
        return '<Owner %r>' % self.name


class OwnerSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "document", "type_document", "properties")

        model = Owner

    properties = ma.Nested("PropertySchema", many=True, exclude=("owners",))


owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)
