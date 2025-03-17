from app import db
from app.models.base import BaseModel
from app.models.place import place_amenity

import uuid



class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with a place.
    """

    __tablename__ = 'amenities'
    _name = db.Column(db.String(50), nullable=False)
    places = db.relationship(
        'Place',
        secondary='place_amenity',
        back_populates='amenities'
    )

    @property
    def name(self):
        """
        Get the amenity's name.
        """
        return self.__name

    @name.setter
    def name(self, value):
        """
        Set the amenity's name.
        """
        if not value or len(value) > 50:
            raise ValueError("Name must be provided and be at most 50 characters long.")
        self._name = value
