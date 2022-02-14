from sqlalchemy import Column, Integer, String

from database import db
from ma import ma


class Property(db.Model):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    real_estate_registration = Column(Integer, nullable=False)
    type_property = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return '<Property %r>' % self.name


class PropertySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id",
            "address",
            "name",
            "real_estate_registration",
            "type_property",
            "owners",
        )
        model = Property
    owners = ma.Nested("OwnerSchema", many=True, exclude=("properties",))


property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)
