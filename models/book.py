from db import db

class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    cover_url = db.Column(db.String)
    author_name = db.Column(db.String(80))

    reviews = db.relationship('ReviewModel', lazy='dynamic')
    
    genre = db.Column(db.String(), db.ForeignKey('genres.name'))
    #genre = db.relationship('GenreModel')

    def __init__(self, name, cover_url, author_name, genre):
        self.name = name
        self.cover_url = cover_url
        self.author_name = author_name
        self.genre = genre

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'cover_url': self.cover_url,
            'author_name': self.author_name,
            'genre': self.genre,
            'reviews': [review.json() for review in self.reviews.all()]

        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    #find by category
    @classmethod
    def find_by_genre(cls, genre):
        return cls.query.filter_by(genre=genre)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
