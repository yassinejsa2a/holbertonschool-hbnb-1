from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request, jsonify
from app.models.user import User
import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', min_length=1, max_length=50),
    'last_name': fields.String(required=True, description='Last name of the user', min_length=1, max_length=50),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.response(200, 'Users list retrieved successfully') 
    def get(self):
        """Get users list"""
        users = facade.get_all_users()
        if not users:
            return {'error': 'No users found'}, 404
        return {'users': [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users]}, 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new user"""
        user_data = api.payload
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        new_user = facade.create_user(user_data)
        
        # Don't include password in the response
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized operation')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload
        for key in user_data:
            if key not in ['first_name', 'last_name', 'email', 'password']:
                return {'error': 'Invalid input data.'}, 400

        current_user = get_jwt_identity()
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403

            if user_data.get('email'):
                if facade.get_user_by_email(user_data['email']):
                    return {'error': 'Email already registered.'}, 400
        else:
            if user_data.get('email') or user_data.get('password'):
                return {'error': 'You cannot modify email or password.'}, 403

            if current_user['id'] != user_id:
                return {'error': 'Unauthorized action.'}, 403

        if not facade.get_user(user_id):
            return {'error': 'User not found.'}, 404

        try:
            facade.update_user(user_id, user_data)
        except Exception as e:
            return {'error': str(e)}, 400

        return self.get(user_id)
