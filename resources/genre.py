from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from models.genre import GenreModel

class Genre(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        "icon_url", type=str, required=True, help="This field cannot be left blank"
    )
    
    @jwt_required()
    def get(self, name):
        genre = GenreModel.find_by_name(name)
        if genre:
            return genre.json()
        return {"message": "Genre not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Admin privilege required."}, 401

        data = Genre.parser.parse_args()

        genre = GenreModel.find_by_name(name)
        if genre:
            return {
                "message": "This book already exists"
            }, 400


        new_genre = GenreModel(name, **data)
        try:
            new_genre.save_to_db()
        except:
            return {"message": "An error occurred inserting a new genre."}, 500

        return new_genre.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Admin privilege required."}, 401

        genre = GenreModel.find_by_name(name)
        if genre:
            genre.delete_from_db()
            return {"message": "Genre deleted."}
        return {"message": "Genre not found."}, 404

    @jwt_required()
    def put(self, name):
        data = Genre.parser.parse_args()

        genre = GenreModel.find_by_name(name)

        if genre:
            genre.name = name
            genre.icon_url = data["icon_url"]
        else:
            return{
                "message": "Genre not found"
            }, 404

        genre.save_to_db()

        return genre.json()

class GenreList(Resource):
    @jwt_required()
    def get(self):
        genres = [genre.json() for genre in GenreModel.find_all()]
        return {"genres": genres}, 200