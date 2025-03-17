from app.models.base import BaseModel
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
import uuid

class Review(BaseModel):
    """
    Represents a review for a place.
    """
    __tablename__ = 'reviews'
    
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Clés étrangères correctement définies
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relations bidirectionnelles
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
