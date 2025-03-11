from ApiRequests.api_requests import ApiRequests
from data.error_messages import ErrorsMessages
from data.expected_results import ExpectedResults
from data.globals import ApiHttpConstants


class TestsBookAPI(ApiRequests):

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
        assert response.status_code == ApiHttpConstants.BAD_REQUEST, ErrorsMessages.ERROR_CANT_RETURNED_BORROWED

        # Teardown: Return the book after the test
        self.post(f"/users/{borrow_data['user_id']}/return/{borrow_data['book_id']}")


    # BUG RETURNING NON BORROWED BOOK MUST NOT BE ALLOWED
    def test_return_book_not_borrowed(self):
        """Test returning a book that hasn't been borrowed."""
        # Attempt to return a book that hasn't been borrowed
        return_data = {"user_id": 1, "book_id": 1}
        returned_suffix = f"/users/{return_data['user_id']}/return/{return_data['book_id']}"
        response = self.post(returned_suffix, json=return_data)
        assert response.status_code == ApiHttpConstants.BAD_REQUEST, ErrorsMessages.ERROR_RETURN_NON_BORROWED

    # Bug deleting borRowed book can't be done!
    def test_delete_borrowed_book(self):
        """Test deleting a book that is currently borrowed."""
        # Borrow a book
        borrow_data = {"user_id": 1, "book_id": 1}
        borrowed_suffix = f"/users/{borrow_data['user_id']}/borrow/{borrow_data['book_id']}"
        response = self.post(borrowed_suffix, json=borrow_data)
        assert response.status_code == ApiHttpConstants.OK

        # Attempt to delete the borrowed book
        response = self.delete(f"/books/{borrow_data['book_id']}")
        assert response.status_code == ApiHttpConstants.CONFLICT,ErrorsMessages.ERROR_CANT_BORROW

        # Teardown: Return the book after the test
        self.post(f"/users/{borrow_data['user_id']}/return/{borrow_data['book_id']}")

    def test_update_book_information(self):
        """Test updating the information of an existing book."""
        # Add a new book
        new_book_data = {"title": "Brave New World", "author": "Aldous Huxley"}
        response = self.post("/books", json=new_book_data)
        assert response.status_code == ApiHttpConstants.CREATED
        new_book = response.json()

        # Update the book's information
        updated_book_data = {"title": "Brave New World - Revised", "author": "Aldous Huxley"}
        response = self.put(f"/books/{new_book['id']}", json=updated_book_data)
        assert response.status_code == ApiHttpConstants.OK

        # Verify the book's information was updated
        response = self.get(f"/books")
        updated_books = response.json()
        updated_book_not_found = False
        for book in updated_books:
            updated_book_not_found=True
            if book["title"]==  ExpectedResults.EXPECTED_UPDATED_BOOK_TITLE2:
                updated_book_not_found=False
                assert book["author"] == ExpectedResults.EXPECTED_BOOK_AUTHOR2, "Book author should remain the same."

        # Teardown: Delete the book after the test
        self.delete(f"/books/{new_book['id']}")
        assert updated_book_not_found==False, f"error in updated book title<>{ExpectedResults.EXPECTED_UPDATED_BOOK_TITLE2}"