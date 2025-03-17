import unittest
from app import create_app, db
from config import DevelopmentConfig

class TestSQLAlchemyConfig(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up test environment"""
        self.app_context.pop()

    def test_sqlalchemy_configuration(self):
        """Test that SQLAlchemy is properly configured"""
        # Check if SQLAlchemy is configured
        self.assertTrue(hasattr(self.app, 'extensions'))
        self.assertTrue('sqlalchemy' in self.app.extensions)
        
        # Test database URI configuration
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///development.db')
        self.assertEqual(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)

    def test_db_instance(self):
        """Test that db instance is properly initialized"""
        # Check that db is a SQLAlchemy instance - compatible with both newer and older versions
        db_class_str = str(type(db))
        self.assertTrue(
            db_class_str == "<class 'flask_sqlalchemy.SQLAlchemy'>" or 
            db_class_str == "<class 'flask_sqlalchemy.extension.SQLAlchemy'>"
        )
        
        # Verify important db attributes
        self.assertTrue(hasattr(db, 'session'))
        self.assertTrue(hasattr(db, 'Model'))
        self.assertTrue(hasattr(db, 'create_all'))
        self.assertTrue(hasattr(db, 'drop_all'))

    def test_repository_pattern(self):
        """Test that SQLAlchemyRepository has required methods"""
        from app.persistence.repository import SQLAlchemyRepository
        from app.models.user import User
        
        # Initialize repository
        repo = SQLAlchemyRepository(User)
        
        # Check required methods
        self.assertTrue(hasattr(repo, 'add'))
        self.assertTrue(hasattr(repo, 'get'))
        self.assertTrue(hasattr(repo, 'get_all'))
        self.assertTrue(hasattr(repo, 'update'))
        self.assertTrue(hasattr(repo, 'delete'))
        self.assertTrue(hasattr(repo, 'get_by_attribute'))

if __name__ == '__main__':
    unittest.main()
