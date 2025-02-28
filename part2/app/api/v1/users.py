from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request, jsonify

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
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
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        try:
            # Check if email already exists
            if facade.get_user_by_email(user_data.get('email')):
                return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

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


    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update an existing user"""
        user_data = api.payload
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        if (
            user.first_name == user_data.get('first_name', user.first_name) and
            user.last_name == user_data.get('last_name', user.last_name) and
            user.email == user_data.get('email', user.email)
        ):
            return {'error': 'No changes detected'}, 400

        if user_data.get('email') and user_data.get('email') != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user.id:
                return {'error': 'Email already registered'}, 400

        try:
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)

            facade.update_user(user.id, user_data)
        except Exception as e:
            return {'error': str(e)}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
