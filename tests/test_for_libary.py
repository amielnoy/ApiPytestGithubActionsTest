from ApiRequests.api_requests import ApiRequests
from app import books
from data.expected_results import ExpectedResults
from data.globals import ApiHttpConstants
import pytest


class TestsBookAPI(ApiRequests):
    """Tests for the book API endpoints."""

    def test_get_books(self):
        response = self.get("/books")
        assert response.status_code == ApiHttpConstants.OK, \
        f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        books = response.json()
        assert len(books) == ExpectedResults.EXPECTED_BOOK_NUMBER, \
            f"Actual book number={len(books)} does not match expected book number={ExpectedResults.EXPECTED_BOOK_NUMBER}"


    def test_books_details(self):
        response = self.get("/books")
        assert response.status_code==ApiHttpConstants.OK, \
        f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        books_details=response.json()

        assert len(books_details)==ExpectedResults.EXPECTED_BOOK_NUMBER, \
            f"Actual book number={len(books)} does not match expected book number={ExpectedResults.EXPECTED_BOOK_NUMBER}"
        # Assuming there are 2 books in the initial setup
        assert books_details[0]["title"] == ExpectedResults.EXPECTED_BOOK_TITLE1, \
            f"Actual book title={books_details[0]["title"]} does not match expected book title={ExpectedResults.EXPECTED_BOOK_TITLE1}"
        assert books_details[1]["title"] == ExpectedResults.EXPECTED_BOOK_TITLE2, \
            f"Actual book title={books_details[1]["title"]} does not match expected book title={ExpectedResults.EXPECTED_BOOK_TITLE2}"


    def test_add_book(self):
        new_book = {"title": "1984", "author": "George Orwell"}
        response = self.post("/books", json=new_book)
        assert response.status_code == ApiHttpConstants.CREATED, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        added_book = response.json()
        assert added_book["title"] == ExpectedResults.EXPECTED_BOOK_TITLE1, \
            f"Actual book title={added_book['title']} does not match expected book title={ExpectedResults.EXPECTED_BOOK_TITLE1}"
        assert added_book["author"] == ExpectedResults.EXPECTED_BOOK_AUTHOR, \
            f"Actual added book author={added_book['author']} does not match expected book author={ExpectedResults.EXPECTED_BOOK_AUTHOR}"

    def test_update_book(self):
        response = self.put("/books/1", json={"title": ExpectedResults.EXPECTED_UPDATED_BOOK_TITLE})
        assert response.status_code == ApiHttpConstants.OK, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        updated_book = response.json()
        assert updated_book["title"] == ExpectedResults.EXPECTED_UPDATED_BOOK_TITLE, \
            f"Actual updated book title={updated_book['title']} does not match expected updated book title={ExpectedResults.EXPECTED_UPDATED_BOOK_TITLE}"

    def test_update_non_exist_book(self):
        response = self.put("/books/10", json={"title": ExpectedResults.EXPECTED_UPDATED_BOOK_TITLE})
        assert response.status_code == ApiHttpConstants.NOT_FOUND, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.NOT_FOUND}"


    def test_delete_book(self):
        response = self.delete("/books/2")
        assert response.status_code == ApiHttpConstants.OK, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        response = self.get("/books")
        assert response.status_code == ApiHttpConstants.OK, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        books = response.json()
        assert len(books) == ExpectedResults.EXPECTED_BOOK_NUMBER, \
            f"Actual numbers of books={len(books)} does not match expected number of books={ExpectedResults.EXPECTED_BOOK_NUMBER}"



    def test_borrow_book(self):
        borrow_data = {"user_id": 1, "book_id": 1}
        borrowed_suffix=f"/users/{borrow_data["user_id"]}/borrow/{borrow_data["book_id"]}"
        response = self.post(borrowed_suffix, json=borrow_data)
        assert response.status_code == ApiHttpConstants.OK, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.OK}"
        borrow_confirmation = response.json()
        assert borrow_confirmation['message'] == ExpectedResults.EXPECTED_BOOK_BORROW_MESSAGE, \
            f"Expected borrow message to be {ExpectedResults.EXPECTED_BOOK_BORROW_MESSAGE}"

    def test_borrow_non_exist_book(self):
        borrow_data = {"user_id": 10, "book_id": 10}
        borrowed_suffix=f"/users/{borrow_data["user_id"]}/borrow/{borrow_data["book_id"]}"
        response = self.post(borrowed_suffix, json=borrow_data)
        assert response.status_code == ApiHttpConstants.NOT_FOUND, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.OK}"

    def test_return_book(self):
        return_data = {"user_id": 1, "book_id": 1}
        returned_suffix = f"/users/{return_data["user_id"]}/return/{return_data["book_id"]}"
        response = self.post(returned_suffix, json=return_data)
        assert response.status_code == ApiHttpConstants.OK, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.OK}"
        return_confirmation = response.json()
        assert return_confirmation['message'] == ExpectedResults.EXPECTED_BOOK_RETURNED_MESSAGE,\
            f"Expected return book message to be {ExpectedResults.EXPECTED_BOOK_RETURNED_MESSAGE}"

    def test_return_non_exist_book(self):
        return_data = {"user_id": 20, "book_id": 20}
        returned_suffix = f"/users/{return_data["user_id"]}/return/{return_data["book_id"]}"
        response = self.post(returned_suffix, json=return_data)
        assert response.status_code == ApiHttpConstants.NOT_FOUND, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.OK}"

    def test_add_and_update_book(self):
        self.test_add_book()
        self.test_update_book()

    def test_add_and_delete_new_book(self):
        self.test_add_book()
        response = self.delete("/books/3")
        assert response.status_code == ApiHttpConstants.OK, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        response = self.get("/books")
        assert response.status_code == ApiHttpConstants.OK, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        books = response.json()
        assert len(books) == ExpectedResults.EXPECTED_BOOK_NUMBER, \
            f"Actual numbers of books={len(books)} does not match expected number of books={ExpectedResults.EXPECTED_BOOK_NUMBER}"


    def test_delete_non_existant_book(self):
        response = self.delete("/books/10")
        assert response.status_code == ApiHttpConstants.NOT_FOUND, \
            f"Expected status code to be {ApiHttpConstants.NOT_FOUND}"

    def test_add_and_double_delete_new_book(self):
        self.test_add_book()
        response = self.delete("/books/3")
        assert response.status_code == ApiHttpConstants.OK, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        response = self.get("/books")
        assert response.status_code == ApiHttpConstants.OK, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.CREATED}"
        books = response.json()
        assert len(books) == ExpectedResults.EXPECTED_BOOK_NUMBER, \
            f"Actual numbers of books={len(books)} does not match expected number of books={ExpectedResults.EXPECTED_BOOK_NUMBER}"

        response = self.delete("/books/3")
        assert response.status_code == ApiHttpConstants.NOT_FOUND, \
            f"Actual response code={response.status_code} does not match expected response code={ApiHttpConstants.NOT_FOUND}"