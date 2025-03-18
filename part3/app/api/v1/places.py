from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Title already registered')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new place"""
        place_data = api.payload
        current_user = get_jwt_identity()
        
        # Check if the user ID is a dictionary and extract the ID
        if isinstance(current_user, dict):
            current_user_id = current_user.get('id')
            is_admin = current_user.get('is_admin', False)
        else:
            current_user_id = current_user
            is_admin = False
            
        # If user ID couldn't be extracted
        if not current_user_id:
            return {'error': 'Could not determine user ID from token'}, 400
        
        # Check authorization - users can only create places for themselves unless they're admins
        if not is_admin and current_user_id != place_data['owner_id']:
            return {'error': 'Unauthorized action - cannot create places for other users'}, 403

        try:
            owner = facade.get_user(place_data['owner_id'])
            if not owner:
                return {'error': 'Owner not found'}, 404

            existing_place = facade.get_place_by_title(place_data['title'])
            if existing_place:
                return {'error': 'Title already registered'}, 400

            new_place = facade.create_place(place_data)
        
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': str(new_place.price),
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [
            {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': str(place.price),
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id,
                'amenities': place.amenities
            }
            for place in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        owner = facade.get_user(place.owner_id)
        owner_data = {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name,
            'email': owner.email
        } if owner else None

        amenity_data = []
        for amenity_id in place.amenities:
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenity_data.append({
                    'id': amenity.id,
                    'name': amenity.name
                })

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': str(place.price),
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_data,
            'amenities': amenity_data
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update place details"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        current_user = get_jwt_identity()
        
        # Check if the user identity is a dictionary and extract the relevant data
        if isinstance(current_user, dict):
            current_user_id = current_user.get('id')
            is_admin = current_user.get('is_admin', False)
        else:
            current_user_id = current_user
            is_admin = False
        
        # If user ID couldn't be extracted
        if not current_user_id:
            return {'error': 'Could not determine user ID from token'}, 400
        
        # Allow update if user is admin or is the owner of the place
        if not is_admin and current_user_id != place.owner_id:
            return {'error': 'Unauthorized action'}, 403

        update_data = api.payload
        try:
            facade.update_place(place_id, update_data)
            updated_place = facade.get_place(place_id)  # Get updated place
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': str(updated_place.price),
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner_id,
                'amenities': updated_place.amenities
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
