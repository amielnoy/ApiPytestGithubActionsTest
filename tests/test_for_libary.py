import pytest
from ApiRequests.api_requests import ApiRequests
from app import books
from data.expected_results import ExpectedResults
from data.globals import ApiHttpConstants


import pytest
from ApiRequests.api_requests import ApiRequests
from data.expected_results import ExpectedResults
from data.globals import ApiHttpConstants


class TestsBookAPI(ApiRequests):
    """Tests for the book API endpoints."""
    def test_get_books(self):
        response = self.get("/books")
        assert response.status_code == ApiHttpConstants.OK
        books = response.json()
        assert len(books) == ExpectedResults.EXPECTED_BOOK_NUMBER, \
            f"Expected {ExpectedResults.EXPECTED_BOOK_NUMBER} books, found {len(books)}."

    @pytest.fixture
    def new_book(self):
        """Fixture for creating a new book."""
        book_data = {"title": "1984", "author": "George Orwell"}
        response = self.post("/books", json=book_data)
        assert response.status_code == ApiHttpConstants.CREATED, \
            f"Failed to add book. Response code={response.status_code}"
        added_book = response.json()
        yield added_book

        # Teardown: Delete the book after the test
        self.delete(f"/books/{added_book['id']}")

    def test_books_details(self):
        response = self.get("/books")
        assert response.status_code == ApiHttpConstants.OK
        books_details = response.json()

        assert len(books_details) == ExpectedResults.EXPECTED_BOOK_NUMBER
        assert books_details[0]["title"] == ExpectedResults.EXPECTED_BOOK_TITLE1
        assert books_details[1]["title"] == ExpectedResults.EXPECTED_BOOK_TITLE3

    def test_add_book(self, new_book):
        assert new_book["title"] == ExpectedResults.EXPECTED_BOOK_TITLE3
        assert new_book["author"] == ExpectedResults.EXPECTED_BOOK_AUTHOR

    def test_update_book(self):
        response = self.put("/books/1", json={"title": ExpectedResults.EXPECTED_UPDATED_BOOK_TITLE})
        assert response.status_code == ApiHttpConstants.OK
        updated_book = response.json()
        assert updated_book["title"] == ExpectedResults.EXPECTED_UPDATED_BOOK_TITLE

        # Restore original title
        response = self.put("/books/1", json={"title": ExpectedResults.EXPECTED_BOOK_TITLE1})
        assert response.status_code == ApiHttpConstants.OK

    def test_update_non_exist_book(self):
        response = self.put("/books/10", json={"title": ExpectedResults.EXPECTED_UPDATED_BOOK_TITLE})
        assert response.status_code == ApiHttpConstants.NOT_FOUND

    def test_delete_book(self):
        # Attempt to delete a specific book with ID 2
        response = self.delete("/books/2")
        assert response.status_code == ApiHttpConstants.OK

        response = self.get("/books")
        assert response.status_code == ApiHttpConstants.OK
        books = response.json()
        assert 2 not in [book['id'] for book in books]

    def test_borrow_book(self):
        borrow_data = {"user_id": 1, "book_id": 1}
        borrowed_suffix = f"/users/{borrow_data['user_id']}/borrow/{borrow_data['book_id']}"
        response = self.post(borrowed_suffix, json=borrow_data)
        assert response.status_code == ApiHttpConstants.OK
        borrow_confirmation = response.json()
        assert borrow_confirmation['message'] == ExpectedResults.EXPECTED_BOOK_BORROW_MESSAGE
    def test_return_book(self):
        return_data = {"user_id": 1, "book_id": 1}
        returned_suffix = f"/users/{return_data['user_id']}/return/{return_data['book_id']}"
        response = self.post(returned_suffix, json=return_data)
        assert response.status_code == ApiHttpConstants.OK
        return_confirmation = response.json()
        assert return_confirmation['message'] == ExpectedResults.EXPECTED_BOOK_RETURNED_MESSAGE

    def test_add_and_delete_new_book(self, new_book):
        pass

    def test_delete_non_exist_book(self):
        response = self.delete("/books/10")
        assert response.status_code == ApiHttpConstants.NOT_FOUND

    def test_sanity_check(self):
        """Sanity test to ensure basic API functionality."""
        # Check if the books endpoint is reachable and returns a status code 200
        response = self.get("/books")
        assert response.status_code == ApiHttpConstants.OK, "Books endpoint is not reachable."

        # Check if the users endpoint is reachable and returns a status code 200
        response = self.get("/users")
        assert response.status_code == ApiHttpConstants.OK, "Users endpoint is not reachable."

        # Check if a non-existent endpoint returns a 404 status code
        response = self.get("/non_existent_endpoint")
        assert response.status_code == ApiHttpConstants.NOT_FOUND, "Non-existent endpoint did not return 404."