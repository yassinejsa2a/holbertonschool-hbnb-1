from app.models.base import BaseModel
from app.models.user import User
from app import db
import uuid
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property


place_amenity = db.Table('place_amenity',
    Column('place_id', Integer, ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenitys.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Numeric(precision=10, scale=1), nullable=False)
    longitude = db.Column(db.Numeric(precision=10, scale=1), nullable=False)
    owner_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    amenities = db.relationship('Amenity', secondary=place_amenity,
                           back_populates='places', cascade='all, delete')

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @hybrid_property
    def title(self):
        """
        Get the place's title.
        """
        return self.__title

    @title.setter
    def title(self, value):
        """
        Set the place's title.
        """
        self.__title = value

    @hybrid_property
    def description(self):
        """
        Get the place's description.
        """
        return self.__description

    @description.setter
    def description(self, value):
        """
        Set the place's description.
        """
        self.__description = value

    @hybrid_property
    def price(self):
        """
        Get the place's price.
        """
        return self.__price

    @price.setter
    def price(self, value):
        """
        Set the place's price.
        """
        if value < 0:
            raise ValueError("price must be >= 0")
        self.__price = value

    @hybrid_property
    def latitude(self):
        """
        Get the place's latitude.
        """
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """
        Set the place's latitude.
        """
        if not isinstance(value, (int, float)):
            raise ValueError('latitude must be a number')
        if value < -90.0 or value > 90.0:
            raise ValueError('latitude must be between -90 and 90')
        self.__latitude = value


    @hybrid_property
    def longitude(self):
        """
        Get the place longitude.
        """
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """
        Set the place longitude.
        """
        if not isinstance(value, (int, float)):
            raise ValueError("longitude must be a number")
        if value < -180.0 or value > 180.0:
            raise ValueError('longitude must be between -180 and 180')
        self.__longitude = value

    @hybrid_property
    def owner(self):
        """
        Get the place owner.
        """
        return self.__owner_id

    @owner.setter
    def owner(self, value):
        """
        Set the place owner.
        """
        self.__owner_id = value
