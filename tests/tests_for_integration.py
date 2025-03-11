from data.globals import ApiHttpConstants
import pytest
from ApiRequests.api_requests import ApiRequests
from data.expected_results import ExpectedResults
from data.globals import ApiHttpConstants


class TestsBookAPI(ApiRequests):

    def test_borrow_and_return_book_flow(self):
        """Test the flow of borrowing and returning a book."""
        # Borrow a book
        borrow_data = {"user_id": 1, "book_id": 1}
        borrowed_suffix = f"/users/{borrow_data['user_id']}/borrow/{borrow_data['book_id']}"
        response = self.post(borrowed_suffix, json=borrow_data)
        assert response.status_code == ApiHttpConstants.OK

        # Check if the book is marked as borrowed
        response = self.get("/books/1")
        assert response.status_code == ApiHttpConstants.OK
        book = response.json()
        assert book["is_borrowed"], "Book should be marked as borrowed."

        # Return the book
        return_data = {"user_id": 1, "book_id": 1}
        returned_suffix = f"/users/{return_data['user_id']}/return/{return_data['book_id']}"
        response = self.post(returned_suffix, json=return_data)
        assert response.status_code == ApiHttpConstants.OK

        # Check if the book is marked as not borrowed
        response = self.get("/books/1")
        assert response.status_code == ApiHttpConstants.OK
        book = response.json()
        assert not book["is_borrowed"], "Book should be marked as not borrowed."

    def test_add_and_borrow_new_book(self):
        """Test adding a new book and then borrowing it."""
        # Add a new book
        new_book_data = {"title": "Brave New World", "author": "Aldous Huxley"}
        response = self.post("/books", json=new_book_data)
        assert response.status_code == ApiHttpConstants.CREATED
        new_book = response.json()

        # Borrow the newly added book
        borrow_data = {"user_id": 1, "book_id": new_book["id"]}
        borrowed_suffix = f"/users/{borrow_data['user_id']}/borrow/{borrow_data['book_id']}"
        response = self.post(borrowed_suffix, json=borrow_data)
        assert response.status_code == ApiHttpConstants.OK

        # Teardown: Return and delete the book after the test
        self.post(f"/users/{borrow_data['user_id']}/return/{borrow_data['book_id']}")
        self.delete(f"/books/{new_book['id']}")

    def test_borrow_already_borrowed_book(self):
        """Test borrowing a book that is already borrowed."""
        # Borrow a book
        borrow_data = {"user_id": 1, "book_id": 1}
        borrowed_suffix = f"/users/{borrow_data['user_id']}/borrow/{borrow_data['book_id']}"
        response = self.post(borrowed_suffix, json=borrow_data)
        assert response.status_code == ApiHttpConstants.OK

        # Attempt to borrow the same book again
        response = self.post(borrowed_suffix, json=borrow_data)
        assert response.status_code == ApiHttpConstants.BAD_REQUEST, "Should not be able to borrow an already borrowed book."

        # Teardown: Return the book after the test
        self.post(f"/users/{borrow_data['user_id']}/return/{borrow_data['book_id']}")