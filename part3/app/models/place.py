from app import db
from app.models.base import BaseModel


place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'
    
    _title = db.Column(db.String(50), nullable=False)
    _description = db.Column(db.String(50), nullable=False)
    _price = db.Column(db.Float, nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)
    _owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places', cascade='all, delete')

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price must be >= 0")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError('latitude must be a number')
        if value < -90.0 or value > 90.0:
            raise ValueError('latitude must be between -90 and 90')
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("longitude must be a number")
        if value < -180.0 or value > 180.0:
            raise ValueError('longitude must be between -180 and 180')
        self._longitude = value

    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        self._owner_id = value
