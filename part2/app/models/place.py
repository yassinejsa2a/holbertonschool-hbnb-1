from app.models.base import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner_id
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @property
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

    @property
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

    @property
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

    @property
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


    @property
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

    @property
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
