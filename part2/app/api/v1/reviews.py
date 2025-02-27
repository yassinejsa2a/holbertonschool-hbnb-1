from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(
        required=True,
        description='Text of the review'
        ),
    'rating': fields.Integer(
        required=True,
        description='Rating of the place (1-5)'
        ),
    'user_id': fields.String(
        required=True,
        description='ID of the user'
        ),
    'place_id': fields.String(
        required=True,
        description='ID of the place'
        )
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        pass

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = []
        for review in facade.get_all_reviews():
            reviews.append(
                {
                    "id": review.id,
                    "text": review.text,
                    "rating": review.rating
                }
                )
        return reviews, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        pass

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        pass
