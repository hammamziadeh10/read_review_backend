from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from models.genre import GenreModel
from models.book import BookModel


class Book(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "cover_url", type=str, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "author_name", type=str, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "genre", type=str, required=True, help="This field cannot be left blank"
    )

    @jwt_required()
    def get(self, id):
        book = BookModel.find_by_id(id)
        if book:
            return book.json()
        return {"message": "Book not found"}, 404

    @jwt_required()
    def post(self):
        data = Book.parser.parse_args()

        for book in BookModel.find_by_name(data["name"]):
            if book.author_name == data["author_name"]:
                return {
                    "message": "This book already exists"
                }, 400

        if not GenreModel.find_by_name(data["genre"]):
            return {"message": "Genre not found"}, 404

        book = BookModel(**data)

        try:
            book.save_to_db()
        except:
            return {"message": "An error occurred inserting the book."}, 500

        return book.json(), 201

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Admin privilege required."}, 401

        book = BookModel.find_by_id(id)
        if book:
            book.delete_from_db()
            return {"message": "Book deleted."}
        return {"message": "Book not found."}, 404

    @jwt_required()
    def put(self, id):
        data = Book.parser.parse_args()

        if not GenreModel.find_by_name(data["genre"]):
            return {"message": "Genre not found"}, 404

        book = BookModel.find_by_id(id)

        if book:
            book.name = data["name"]
            book.cover_url = data["cover_url"]
            book.author_name = data["author_name"]
            book.genre = data["genre"]
        else:
            return{
                "message": "Book not found"
            }, 404

        book.save_to_db()

        return book.json()


class BookList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "genre", type=str, required=False, help="This field cannot be left blank"
    )

    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        data = BookList.parser.parse_args()

        if data["genre"]:
            books = [book.json() for book in BookModel.find_by_genre(data["genre"])]
        else:
            books = [book.json() for book in BookModel.find_all()]
        
        if not user_id:
            return {
                "books": [book["name"] for book in books],
                "message": "More data available if you log in.",
            }, 200
        return {"books": books}, 200

