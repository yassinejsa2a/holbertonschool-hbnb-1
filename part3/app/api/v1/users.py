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

    @api.expect(api.model('UserUpdate', {
        'first_name': fields.String(description='First name of the user', min_length=1, max_length=50),
        'last_name': fields.String(description='Last name of the user', min_length=1, max_length=50),
        'email': fields.String(description='Email of the user'),
        'password': fields.String(description='Password of the user')
    }), validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized operation')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user details - Regular users can only update own first/last name, admins can update any user's details"""
        user_data = api.payload
        user = facade.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        # Get current user identity and check admin status
        current_user_id = get_jwt_identity()
        is_admin = current_user_id.get('is_admin', False)
        
        # If not admin, restrict to own profile and only first/last name
        if not is_admin:
            if str(user.id) != str(current_user_id):
                return {'error': 'Unauthorized action.'}, 403
            
            # Check if user is trying to modify email or password
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password.'}, 400
            
            # Check if there are actual changes
            if (
                user.first_name == user_data.get('first_name', user.first_name) and
                user.last_name == user_data.get('last_name', user.last_name)
            ):
                return {'error': 'No changes detected'}, 400
            
            # Update first_name and last_name only
            try:
                update_data = {
                    'first_name': user_data.get('first_name', user.first_name),
                    'last_name': user_data.get('last_name', user.last_name)
                }
                facade.update_user(user.id, update_data)
                user.first_name = update_data['first_name']
                user.last_name = update_data['last_name']
            except Exception as e:
                return {'error': str(e)}, 400
            
        # Admin can modify any field
        else:
            update_data = {}
            
            # For each field in the payload, check and update
            if 'first_name' in user_data:
                update_data['first_name'] = user_data['first_name']
            if 'last_name' in user_data:
                update_data['last_name'] = user_data['last_name']
            
            # Check email uniqueness if changing email
            if 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and str(existing_user.id) != str(user_id):
                    return {'error': 'Email is already in use'}, 400
                update_data['email'] = user_data['email']
            
            # Handle password update
            if 'password' in user_data:
                hashed_password = user.hash_password(user_data['password'])
                update_data['password'] = hashed_password
            
            # If no changes to apply
            if not update_data:
                return {'error': 'No changes detected'}, 400
                
            try:
                facade.update_user(user.id, update_data)
                # Update user object with new values for response
                for key, value in update_data.items():
                    setattr(user, key, value)
            except Exception as e:
                return {'error': str(e)}, 400
        
        # Return updated user details
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
