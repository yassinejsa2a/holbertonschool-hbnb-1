from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user


    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if user:
            self.user_repo.update(user_id, user_data)


    def get_user(self, user_id):
        return self.user_repo.get(user_id)


    def get_all_users(self):
        return self.user_repo.get_all()


    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # Place
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place_by_title(self, title):
        return self.place_repo.get_by_attribute('title', title)
