# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from sqlalchemy import String


# Base that adds dataclass behaviors to mapped classes
class Base(MappedAsDataclass, DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


from isbnlib import is_isbn10, is_isbn13, meta, clean

class Book(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(256), nullable=True, default=None)
    authors: Mapped[str] = mapped_column(String(256), nullable=True, default=None)
    publisher: Mapped[str] = mapped_column(String(128), nullable=True, default=None)
    year: Mapped[str] = mapped_column(String(10), nullable=True, default=None)

    def __post_init__(self):
        # Only auto-populate if only ISBN is provided (other fields are None)
        if self.isbn and not (self.title or self.authors or self.publisher or self.year):
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
