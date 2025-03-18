from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import create_access_token
import datetime

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class AuthResource(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """User login endpoint"""
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])
        
        if not user:
            return {'message': 'Invalid credentials'}, 401
            
        # Check if we're using bcrypt correctly
        if not user.verify_password(credentials['password']):
            return {'message': 'Invalid credentials'}, 401
        
        # Generate JWT token with proper claims
        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })
        return {'access_token': access_token}, 200