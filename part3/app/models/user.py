from app.models.base import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__() 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = password
        places = db.relationship('Place',
                             back_populates='owner',
                             cascade='all, delete-orphan')

    def add_place(self, place):
        """Add a place to the user"""
        self.places.append(place)


    def add_review(self, review):
        """Add a review to the user"""
        self.reviews.append(review)


    @hybrid_property
    def first_name(self):
        """
        Get the user's first name.
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """
        Set the user's first name.
        """
        if not value or len(value) > 50 or len(value) < 1:
            raise ValueError(
                'The first name must be indicated and must be less than 50 characters long.'
                )
        self.__first_name = value

    @hybrid_property
    def last_name(self):
        """
        Get the user's last name.
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """
        Set the user's last name.
        """
        if not value or len(value) > 50 or len(value) < 1:
            raise ValueError(
                'The last name must be indicated and must be less than 50 characters long.'
                )
        self.__last_name = value

    @hybrid_property
    def email(self):
        """
        Get the user's email.
        """
        return self.__email

    @email.setter
    def email(self, value):
        """
        Set the user's email.
        """
        if not isinstance(value, str) or '@' not in value:
            raise ValueError("Valid email is required")
        self.__email = value

    @hybrid_property
    def is_admin(self):
        """
        Get the user's admin status.
        """
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        """
        Set the user's admin status.
        """
        if not isinstance(value, bool):
            raise ValueError('is_admin must be a boolean')
        self.__is_admin = value

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)