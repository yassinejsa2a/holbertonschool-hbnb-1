from app.models.base import BaseModel
from app.models.user import User
from app.models.place import Place
from sqlalchemy.ext.hybrid import hybrid_property
from app import db
import uuid

class Review(db.Model, BaseModel):
    """
    Represents a review for a place.
    """
    __tablename__ = 'reviews'
    
    text = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36),
                         db.ForeignKey('places.id'),
                         nullable=False)
    user_id = db.Column(db.String(36),
                        db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship('User', back_populates='reviews')
    place = db.relationship('Place', back_populates='reviews')
    
    def __init__(self, text, rating, place_id, user_id):
        """
        Initialize a new review.
        """
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
    
    @hybrid_property
    def text(self):
        """
        Get the review text.
        """
        return self.__text
    
    @text.setter
    def text(self, value):
        """
        Set the review text.
        """
        if not value:
            raise ValueError("Review text cannot be empty")
        if not isinstance(value, str):
            raise ValueError("Review text must be a string")
        self.__text = value
    
    @hybrid_property
    def rating(self):
        """
        Get the rating of the review.
        """
        return self.__rating
    
    @rating.setter
    def rating(self, value):
        """
        Set the rating of the review.
        """
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.__rating = value
    
    @hybrid_property
    def place_id(self):
        """
        Get the place ID being reviewed.
        """
        return self.__place_id
    
    @place_id.setter
    def place_id(self, value):
        """
        Set the place ID being reviewed.
        """
        if not isinstance(value, str):
            raise ValueError("Place ID must be a string")
        self.__place_id = value
    
    @hybrid_property
    def user_id(self):
        """
        Get the user ID who wrote the review.
        """
        return self.__user_id
    
    @user_id.setter
    def user_id(self, value):
        """
        Set the user ID who wrote the review.
        """
        if not isinstance(value, str):
            raise ValueError("User ID must be a string")
        self.__user_id = value
