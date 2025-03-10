import requests

from ApiRequests.api_requests import ApiRequests
from data.globals import ApiHttpConstants


class TestUserAPI(ApiRequests):
    """Tests for the user API endpoints."""

    def test_get_users_number(self):
        response = self.get("/users")
        assert response.status_code == ApiHttpConstants.OK
        users = response.json()
        assert len(users) == 2

    def test_get_users_list(self):
        response = self.get("/users")
        assert response.status_code == ApiHttpConstants.OK
        users = response.json()
        assert isinstance(users, list), "Expected a list of users"
        # Check that each user in the list has the expected keys
        for user in users:
            assert 'id' in user, "User should have an 'id' key"
            assert 'name' in user, "User should have a 'name' key"


    def test_get_users_with_wrong_url_suffix(self):
        response = self.get("/user")
        assert response.status_code == ApiHttpConstants.NOT_FOUND
        # Assumes two initial users

