from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from models.review import ReviewModel
from models.book import BookModel
from models.user import UserModel


class Review(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        "text", type=str, required=True, help="This field cannot be left blank"
    )

    @jwt_required()
    def get(self, id):
        review = ReviewModel.find_by_id(id)
        if review:
            return review.json()
        return {"message": "Review not found"}, 404

    @jwt_required()
    def post(self):
        post_parser = Review.parser.copy()

        post_parser.add_argument(
            "book_id", type=str, required=True, help="This field cannot be left blank"
        )

        data = post_parser.parse_args()

        username = UserModel.find_by_id(get_jwt_identity()).username
        
        if ReviewModel.find_by_user_and_book(username, data["book_id"]):
            return {
                "message": "User review for this book already exists"
            }, 400

        if not BookModel.find_by_id(data["book_id"]):
            return {
                "message": "Incorrect book_id"
            }, 400

        review = ReviewModel(username, **data)
        try:
            review.save_to_db()
        except:
            return {"message": "An error occurred inserting the review."}, 500

        return review.json(), 201

    @jwt_required()
    def delete(self, id):
       
        review = ReviewModel.find_by_id(id)
        if review:
            review.delete_from_db()
            return {"message": "Review deleted."}
        return {"message": "Review not found."}, 404

    @jwt_required()
    def put(self, id):
        data = Review.parser.parse_args()

        review = ReviewModel.find_by_id(id)

        if review:
            review.text = data["text"]
        else:
            return{
                "message": "Review not found"
            }, 404

        review.save_to_db()

        return review.json()