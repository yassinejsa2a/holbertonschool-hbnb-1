from app.models.base import BaseModel
from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(BaseModel):
    """User model class"""
    __tablename__ = 'users'

    # Database columns
    _first_name = db.Column('first_name', db.String(50), nullable=False)
    _last_name = db.Column('last_name', db.String(50), nullable=False)
    _email = db.Column('email', db.String(120), nullable=False, unique=True)
    _password = db.Column('password', db.String(128), nullable=False)
    _is_admin = db.Column('is_admin', db.Boolean, default=False)
    
    # Relationships
    places = db.relationship('Place', back_populates='owner', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    
    """def __init__(self, **kwargs):
        # Extract attributes that need special handling
        first_name = kwargs.pop('first_name', None)
        last_name = kwargs.pop('last_name', None)
        email = kwargs.pop('email', None)
        password = kwargs.pop('password', None)
        is_admin = kwargs.pop('is_admin', False)
        
        # Call parent constructor first
        super().__init__(**kwargs)
        
        # Now set our attributes through their properties
        if first_name:
            self._first_name = first_name
        if last_name:
            self._last_name = last_name
        if email:
            self._email = email
        if password:
            self._password = bcrypt.generate_password_hash(password).decode('utf-8')
        self._is_admin = is_admin"""
    
    # Hybrid properties with getters and setters
    @hybrid_property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("First name must be provided and be at most 50 characters long.")
        self._first_name = value
    
    @hybrid_property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Last name must be provided and be at most 50 characters long.")
        self._last_name = value
    
    @hybrid_property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not value or '@' not in value or len(value) > 120:
            raise ValueError("Valid email must be provided and be at most 120 characters long.")
        self._email = value
    
    @hybrid_property
    def password(self):
        # Don't return the actual hash
        return None
    
    @password.setter
    def password(self, value):
        if not value:
            raise ValueError("Password cannot be empty")
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')
    
    @hybrid_property
    def is_admin(self):
        return self._is_admin
    
    @is_admin.setter
    def is_admin(self, value):
        self._is_admin = bool(value)
    
    def verify_password(self, password):
        """Verify a password against the stored hash."""
        return bcrypt.check_password_hash(self._password, password)
    
    def hash_password(self, password):
        """
        Hash a password and store it in the _password attribute.
        This method is provided for backward compatibility with existing code.
        """
        if not password:
            raise ValueError("Password cannot be empty")
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')
        return self._password
