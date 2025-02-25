from app.models.base import BaseModel
from app.models.user import User

class Review(BaseModel):
    """
    Represents a review of a place.
    """
    def __init__(self, text,rating, user_id, place_id):
        """
        Initialize a new review.
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    @property
    def text(self):
        """
        Get the review's text.
        """
        return self.__text
    
    @text.setter
    def text(self, value):
        """
        Set the review's text.
        """
        self.__text = value

    @property
    def rating(self):
        """
        Get the review's rating.
        """
        return self.__rating
    
    @rating.setter
    def rating(self, value):
        """
        Set the review's rating.
        """
        self.__rating = value

    @property
    def user_id(self):
        """
        Get the review's user_id.
        """
        return self.__user_id
    
    @user_id.setter
    def user_id(self, value):
        """
        Set the review's user_id.
        """
        self.__user_id = value

    @property
    def place_id(self):
        """
        Get the review's place_id.
        """
        return self.__place_id
    
    @place_id.setter
    def place_id(self, value):
        """
        Set the review's place_id.
        """
        self.__place_id = value
