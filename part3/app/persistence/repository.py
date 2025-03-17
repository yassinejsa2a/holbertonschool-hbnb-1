from abc import ABC, abstractmethod
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app import db

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy implementation of the Repository.
    """

    def __init__(self, model):
        """
        Initialize the repository with the model to use.
        """
        self.model = model

    def add(self, obj):
        """
        Add an object to the database.
        """
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """
        Get an object from the database by its ID.
        """
        return db.session.query(self.model).get(obj_id)

    def get_all(self):
        """
        Get all objects from the database.
        """
        return db.session.query(self.model).all()

    def update(self, obj_id, **data):
        """
        Update an object in the database.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """
        Delete an object from the database by its ID.
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """
        Get an object from the database by a specific attribute.
        """
        return db.session.query(self.model).filter_by(**{attr_name: attr_value}).first()

class PlaceRepository(SQLAlchemyRepository):
    """
    Repository for Place objects.
    """

    def __init__(self):
        """
        Initialize the repository with the Place model.
        """
        super().__init__(Place)

    def get_place_by_title(self, title):
        """
        Get a place from the database by a specific title.
        """
        return self.model.query.filter_by(title = title).first()

class ReviewRepository(SQLAlchemyRepository):
    """
    Repository for Review objects.
    """

    def __init__(self):
        """
        Initialize the repository with the Review model.
        """
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        """
        Get a review from the database by a place.
        """
        return self.model.query.filter_by(place_id = place_id).all()

class AmenityRepository(SQLAlchemyRepository):
    """
    Repository for Amenity objects.
    """

    def __init__(self):
        """
        Initialize the repository with the Amenity model.
        """
        super().__init__(Amenity)

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()