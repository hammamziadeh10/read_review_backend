from db import db

class ReviewModel(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    username = db.Column(db.String(80))
    text = db.Column(db.String)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship('BookModel')

    def __init__(self, username, book_id, text):
        self.username = username
        self.book_id = book_id
        self.text = text

    def json(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'username': self.username,
            'text': self.text
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_book_id(cls, book_id):
        return cls.query.filter_by(book_id=book_id)
    
    @classmethod
    def find_by_user_and_book(cls, username, book_id):
        return cls.query.filter_by(book_id=book_id, username=username).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

