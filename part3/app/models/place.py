from app import db
from app.models.base import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property


place_amenity = db.Table(
    'place_amenity',
    db.Column(
        'place_id',
        db.String(36),
        db.ForeignKey('places.id'),
        primary_key=True
    ),
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True
    )
)


class Place(BaseModel):
    """
    Class representing a place.
    """

    __tablename__ = 'places'

    _title = db.Column(db.String(255), nullable=False)
    _description = db.Column(db.Text, nullable=True)
    _price = db.Column(db.Numeric(10, 2), nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)
    _owner_id = db.Column(db.String(36),
                          db.ForeignKey('users.id'),
                          nullable=False)
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review',
                              back_populates='place',
                              cascade='all, delete-orphan')
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        back_populates='places',
        cascade='all, delete'
    )


    @hybrid_property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or len(value) > 255:
            raise ValueError("Title must be provided and be at most 255 characters long.")
        self._title = value

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value and not isinstance(value, str) or len(value) > 2048:
            raise ValueError(
                "Description must be a string of at most 2048 characters."
            )
        self._description = value

    @hybrid_property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price must be >= 0")
        self._price = value

    @hybrid_property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError('latitude must be a number')
        if value < -90.0 or value > 90.0:
            raise ValueError('latitude must be between -90 and 90')
        self._latitude = value

    @hybrid_property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("longitude must be a number")
        if value < -180.0 or value > 180.0:
            raise ValueError('longitude must be between -180 and 180')
        self._longitude = value

    @hybrid_property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not isinstance(value, str) or len(value) != 36:
            raise ValueError(
                'Owner ID must be a string of 36 characters.'
            )
        self._owner_id = value
