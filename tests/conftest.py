import pytest
from ApiRequests.api_requests import ApiRequests
from data.globals import ApiHttpConstants

@pytest.fixture(autouse=True)
def setup_and_teardown():
    api_requests = ApiRequests()
    delete_all_books(api_requests)  # Ensure there are no pre-existing books
    create_test_books(api_requests) # Create a known set of books for testing

def create_test_books(api_requests):
    for book in [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"title": "1984", "author": "George Orwell"}
    ]:
        response = api_requests.post("/books", json=book)
        assert response.status_code == ApiHttpConstants.CREATED, \
            f"Failed to add book. Response code={response.status_code}."

def delete_all_books(api_requests):
    """Delete all books in the database to ensure a clean state."""
    response = api_requests.get("/books")
    if response.status_code == ApiHttpConstants.OK:
        books = response.json()
        for book in books:
            delete_response = api_requests.delete(f"/books/{book['id']}")
            assert delete_response.status_code == ApiHttpConstants.OK, \
                f"Failed to delete book id {book['id']}. Response code={delete_response.status_code}."