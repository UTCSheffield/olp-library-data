# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from isbnlib import is_isbn10, is_isbn13, meta, clean
import csv


# Base that adds dataclass behaviors to mapped classes
class Base(MappedAsDataclass, DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Book(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(256), nullable=True,
                                       default=None)
    authors: Mapped[str] = mapped_column(String(256), nullable=True,
                                         default=None)
    publisher: Mapped[str] = mapped_column(String(128), nullable=True,
                                           default=None)
    year: Mapped[str] = mapped_column(String(10), nullable=True, default=None)

    def __post_init__(self):
        # Only auto-populate if only ISBN is provided (other fields are None)
        if self.isbn and not (self.title or self.authors or self.publisher or
                              self.year):
            isbn = clean(self.isbn)
            if not (is_isbn10(isbn) or is_isbn13(isbn)):
                raise ValueError(f"Invalid ISBN: {isbn}")
            data = meta(isbn, service="openl")
            if not data:
                raise ValueError(f"No data found for ISBN: {isbn}")
            self.title = data.get('Title')
            self.authors = ", ".join(data.get('Authors', []))
            self.publisher = data.get('Publisher')
            self.year = data.get('Year')

    def __repr__(self):
        return f"<Book {self.isbn} - {self.title} by {self.authors}>"

    @property
    def cover_url(self):
        if self.isbn:
            return f"https://covers.openlibrary.org/b/isbn/{self.isbn}-M.jpg"
        return None


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Seed initial books if they don't exist
        if Book.query.count() == 0:
            csv_file = 'books.csv'
            with open(csv_file, newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if Book.query.filter_by(isbn=row['isbn']).first():
                        continue  # Skip if already exists
                    book = Book(
                        isbn=row['isbn'],
                        title=row['title'],
                        authors=row['authors'],
                        publisher=row['publisher'],
                        year=row['year']
                    )
                    db.session.add(book)
                db.session.commit()
        print(f"Imported books from {csv_file}")
