import requests

from ApiRequests.requests_base import RequestsBaseApi

class ApiRequests(RequestsBaseApi):
    def post(self, endpoint, data=None, json=None, **kwargs):
        """Make a POST request."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.post(url, data=data, json=json, **kwargs)
        return response

    def delete(self, endpoint, **kwargs):
        """Make a DELETE request."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.delete(url, **kwargs)
        return response

    def put(self, endpoint, data=None, json=None, **kwargs):
        """Make a PUT request."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.put(url, data=data, json=json, **kwargs)
        return response

    def get(self, endpoint, params=None, **kwargs):
        """Make a GET request."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, params=params, **kwargs)
        return response
