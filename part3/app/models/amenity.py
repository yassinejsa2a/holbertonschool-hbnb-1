from app import db
from app.models.base import BaseModel


class Amenity(BaseModel):
    """
    Class representing an amenity.
    """

    __tablename__ = 'amenities'

    _name = db.Column(db.String(128), nullable=False, unique=True)

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
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the amenity's name.
        """
        if not value or len(value) > 50:
            raise ValueError("Name must be provided and be at most 50 characters long.")
        self._name = value
