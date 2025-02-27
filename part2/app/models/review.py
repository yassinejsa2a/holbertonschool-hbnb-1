from app.models.base import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    """
    Represents a review of a place.
    """
    def __init__(self, text, rating, user, place):
        """
        Initialize a new review.
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

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
        if not value or len(value) > 500:
            raise ValueError('Review text must be provided and be less than 500 characters long.')
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
        if not (1 <= value <= 5):
            raise ValueError('Rating must be between 1 and 5.')
        self.__rating = value

    @property
    def user(self):
        """
        Get the review's user.
        """
        return self.__user
    
    @user.setter
    def user(self, value):
        """
        Set the review's user.
        """
        if not isinstance(value, User):
            raise ValueError('user must be an instance of User.')
        if not value.exists():
            raise ValueError('User does not exist.')
        self.__user = value

    @property
    def place(self):
        """
        Get the review's place.
        """
        return self.__place
    
    @place.setter
    def place(self, value):
        """
        Set the review's place.
        """
        if not isinstance(value, Place):
            raise ValueError('place must be an instance of Place.')
        if not value.exists():
            raise ValueError('Place does not exist.')
        self.__place = value
