from app import db
from app.models.base import BaseModel

class Review(BaseModel):
    """
    Represents a review for a place.
    """
    __tablename__ = 'reviews'
    
    _text = db.Column(db.String(50), nullable=False)
    _rating = db.Column(db.Integer, nullable=False)
    _place_id = db.Column(db.String(36),
                         db.ForeignKey('places.id'),
                         nullable=False)
    _user_id = db.Column(db.String(36),
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
    
    @property
    def text(self):
        """
        Get the review text.
        """
        return self._text
    
    @text.setter
    def text(self, value):
        """
        Set the review text.
        """
        if not value:
            raise ValueError("Review text cannot be empty")
        if not isinstance(value, str):
            raise ValueError("Review text must be a string")
        self._text = value
    
    @property
    def rating(self):
        """
        Get the rating of the review.
        """
        return self._rating
    
    @rating.setter
    def rating(self, value):
        """
        Set the rating of the review.
        """
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value
    
    @property
    def place_id(self):
        """
        Get the place ID being reviewed.
        """
        return self._place_id
    
    @place_id.setter
    def place_id(self, value):
        """
        Set the place ID being reviewed.
        """
        if not isinstance(value, str):
            raise ValueError("Place ID must be a string")
        self._place_id = value
    
    @property
    def user_id(self):
        """
        Get the user ID who wrote the review.
        """
        return self._user_id
    
    @user_id.setter
    def user_id(self, value):
        """
        Set the user ID who wrote the review.
        """
        if not isinstance(value, str):
            raise ValueError("User ID must be a string")
        self._user_id = value
