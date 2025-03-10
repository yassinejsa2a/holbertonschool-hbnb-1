import unittest
from unittest.mock import patch, MagicMock
import pytest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.api.v1.users import UserList, UserResource
from app.api.v1.reviews import ReviewList, ReviewResource
from app.api.v1.places import PlaceList, PlaceResource
from app.api.v1.amenities import AmenityList, AmenityResource

# Import the modules to test


class TestUserModel(unittest.TestCase):
    def test_user_init(self):
        user = User("John", "Doe", "john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)

    def test_user_init_with_admin(self):
        user = User("Admin", "User", "admin@example.com", True)
        self.assertEqual(user.first_name, "Admin")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.email, "admin@example.com")
        self.assertTrue(user.is_admin)

    def test_first_name_validation(self):
        with self.assertRaises(ValueError):
            User("", "Doe", "john.doe@example.com")

        with self.assertRaises(ValueError):
            User("A" * 51, "Doe", "john.doe@example.com")

    def test_last_name_validation(self):
        with self.assertRaises(ValueError):
            User("John", "", "john.doe@example.com")

        with self.assertRaises(ValueError):
            User("John", "D" * 51, "john.doe@example.com")

    def test_email_validation(self):
        with self.assertRaises(ValueError):
            User("John", "Doe", "invalid-email")

        with self.assertRaises(ValueError):
            User("John", "Doe", 123)  # Not a string


class TestPlaceModel(unittest.TestCase):
    def test_place_init(self):
        place = Place(
            "Beach House", "Beautiful beach house", 100.0, 34.5, -118.2, "user_id_123"
        )
        self.assertEqual(place.title, "Beach House")
        self.assertEqual(place.description, "Beautiful beach house")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 34.5)
        self.assertEqual(place.longitude, -118.2)
        self.assertEqual(place.owner_id, "user_id_123")
        self.assertEqual(place.amenities, [])

    def test_price_validation(self):
        with self.assertRaises(ValueError):
            Place(
                "Beach House",
                "Beautiful beach house",
                -10.0,
                34.5,
                -118.2,
                "user_id_123",
            )

    def test_latitude_validation(self):
        with self.assertRaises(ValueError):
            Place(
                "Beach House",
                "Beautiful beach house",
                100.0,
                91.0,
                -118.2,
                "user_id_123",
            )

        with self.assertRaises(ValueError):
            Place(
                "Beach House",
                "Beautiful beach house",
                100.0,
                -91.0,
                -118.2,
                "user_id_123",
            )

        with self.assertRaises(ValueError):
            Place(
                "Beach House",
                "Beautiful beach house",
                100.0,
                "invalid",
                -118.2,
                "user_id_123",
            )

    def test_longitude_validation(self):
        with self.assertRaises(ValueError):
            Place(
                "Beach House",
                "Beautiful beach house",
                100.0,
                34.5,
                181.0,
                "user_id_123",
            )

        with self.assertRaises(ValueError):
            Place(
                "Beach House",
                "Beautiful beach house",
                100.0,
                34.5,
                -181.0,
                "user_id_123",
            )

        with self.assertRaises(ValueError):
            Place(
                "Beach House",
                "Beautiful beach house",
                100.0,
                34.5,
                "invalid",
                "user_id_123",
            )


class TestReviewModel(unittest.TestCase):
    def test_review_init(self):
        review = Review("Great place!", 5, "user_id_123", "place_id_456")
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user_id, "user_id_123")
        self.assertEqual(review.place_id, "place_id_456")

    def test_text_validation(self):
        with self.assertRaises(ValueError):
            Review("", 5, "user_id_123", "place_id_456")

        with self.assertRaises(ValueError):
            Review("A" * 501, 5, "user_id_123", "place_id_456")

    def test_rating_validation(self):
        with self.assertRaises(ValueError):
            Review("Great place!", 0, "user_id_123", "place_id_456")

        with self.assertRaises(ValueError):
            Review("Great place!", 6, "user_id_123", "place_id_456")


class TestAmenityModel(unittest.TestCase):
    def test_amenity_init(self):
        amenity = Amenity("WiFi")
        self.assertEqual(amenity.name, "WiFi")

    def test_name_validation(self):
        with self.assertRaises(ValueError):
            Amenity("")

        with self.assertRaises(ValueError):
            Amenity("A" * 51)


@patch("app.services.facade")
class TestUserAPI(unittest.TestCase):
    def test_get_all_users(self, mock_facade):
        user1 = MagicMock()
        user1.id = "1"
        user1.first_name = "John"
        user1.last_name = "Doe"
        user1.email = "john@example.com"

        mock_facade.get_all_users.return_value = [user1]

        user_list = UserList()
        response = user_list.get()

        self.assertEqual(response[0]["users"][0]["id"], "1")
        self.assertEqual(response[0]["users"][0]["first_name"], "John")
        self.assertEqual(response[1], 200)

    def test_create_user(self, mock_facade):
        mock_facade.get_user_by_email.return_value = None

        new_user = MagicMock()
        new_user.id = "1"
        new_user.first_name = "Jane"
        new_user.last_name = "Smith"
        new_user.email = "jane@example.com"

        mock_facade.create_user.return_value = new_user

        user_list = UserList()
        user_list.api = MagicMock()
        user_list.api.payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
        }

        response = user_list.post()
        self.assertEqual(response[0]["id"], "1")
        self.assertEqual(response[0]["first_name"], "Jane")
        self.assertEqual(response[1], 201)


@patch("app.services.facade")
class TestReviewAPI(unittest.TestCase):
    def test_get_all_reviews(self, mock_facade):
        review1 = MagicMock()
        review1.id = "1"
        review1.text = "Great place!"
        review1.rating = 5

        mock_facade.get_all_reviews.return_value = [review1]

        review_list = ReviewList()
        response = review_list.get()

        self.assertEqual(response[0][0]["id"], "1")
        self.assertEqual(response[0][0]["text"], "Great place!")
        self.assertEqual(response[0][0]["rating"], 5)
        self.assertEqual(response[1], 200)


@patch("app.services.facade")
class TestAmenityAPI(unittest.TestCase):
    def test_create_amenity(self, mock_facade):
        new_amenity = MagicMock()
        new_amenity.id = "1"
        new_amenity.name = "WiFi"

        mock_facade.create_amenity.return_value = new_amenity

        amenity_list = AmenityList()
        amenity_list.api = MagicMock()
        amenity_list.api.payload = {"name": "WiFi"}

        response = amenity_list.post()
        self.assertEqual(response[0]["id"], "1")
        self.assertEqual(response[0]["name"], "WiFi")
        self.assertEqual(response[1], 201)

    def test_get_all_amenities(self, mock_facade):
        amenity1 = MagicMock()
        amenity1.id = "1"
        amenity1.name = "WiFi"

        mock_facade.get_all_amenities.return_value = [amenity1]

        amenity_list = AmenityList()
        response = amenity_list.get()

        self.assertEqual(response[0][0]["id"], "1")
        self.assertEqual(response[0][0]["name"], "WiFi")
        self.assertEqual(response[1], 200)

    def test_get_amenity_by_id(self, mock_facade):
        amenity = MagicMock()
        amenity.id = "1"
        amenity.name = "WiFi"

        mock_facade.get_amenity.return_value = amenity

        amenity_resource = AmenityResource()
        response = amenity_resource.get("1")

        self.assertEqual(response[0]["id"], "1")
        self.assertEqual(response[0]["name"], "WiFi")
        self.assertEqual(response[1], 200)
