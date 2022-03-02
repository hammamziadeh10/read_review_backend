from db import db

class GenreModel(db.Model):
    __tablename__ = 'genres'

    name = db.Column(db.String(80), primary_key=True)
    icon_url = db.Column(db.String)

    books = db.relationship('BookModel', lazy='dynamic')

    def __init__(self, name, icon_url):
        self.name = name
        self.icon_url = icon_url

    def json(self):
        return {
            'name': self.name,
            'icon_url': self.icon_url,
            #'books': [book.json() for book in self.books.all()]

        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
