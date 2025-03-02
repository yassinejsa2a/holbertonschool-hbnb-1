from app.models.base import BaseModel

class Review(BaseModel):
    """
    Represents a review for a place.
    """
    
    def __init__(self, text, rating, place_id, user_id):
        """
        Initialize a new review.
        
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
    
    @property
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
    
    @property
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
    
    @property
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
    
    @property
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
