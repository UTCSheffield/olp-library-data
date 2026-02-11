# populate_books.py
"""
Script to read ISBNs from isbn.txt, fetch book data using isbnlib, and populate the Book table.
"""
import os
from flask import Flask
from models import db, Book
from isbnlib import is_isbn10, is_isbn13, meta, clean

# Use Open Library as the metadata provider
META_PROVIDER = 'openl'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///books.db')
db.init_app(app)

ISBN_FILE = 'isbn.txt'

def valid_isbn(isbn):
    isbn = clean(isbn)
    return is_isbn10(isbn) or is_isbn13(isbn)

def fetch_book_data(isbn):
    try:
        data = meta(isbn, service=META_PROVIDER)
        return data
    except Exception as e:
        print(f"Error fetching data for ISBN {isbn}: {e}")
        return None


def populate_books(test_mode=False, test_limit=5):
    """
    Populate books from ISBN_FILE. If test_mode is True, only process test_limit books.
    """
    with app.app_context():
        db.create_all()
        count = 0
        with open(ISBN_FILE) as f:
            for line in f:
                isbn = line.strip()
                if not isbn:
                    continue
                if Book.query.filter_by(isbn=isbn).first():
                    print(f"Book already exists: {isbn}")
                    continue
                try:
                    book = Book(isbn=isbn)
                except Exception as e:
                    print(f"Error creating Book for ISBN {isbn}: {e}")
                    continue
                db.session.add(book)
                print(f"Added: {isbn} - {book.title}")
                count += 1
                if test_mode and count >= test_limit:
                    print(f"Test mode: processed {test_limit} books. Stopping early.")
                    break
            db.session.commit()

if __name__ == "__main__":
    # Set test_mode=True to only process a few books for testing
    populate_books(test_mode=True, test_limit=5)
