from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

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
        self.__name = value