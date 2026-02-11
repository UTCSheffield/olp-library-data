import csv
from models import db, Book
from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'sqlite:///books.db')
db.init_app(app)

CSV_FILE = 'books_export.csv'


# Export all Book records to CSV
def export_books_to_csv():
    with app.app_context():
        books = Book.query.all()
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['isbn', 'title', 'authors', 'publisher', 'year'])
            for book in books:
                writer.writerow([
                    book.isbn,
                    book.title or '',
                    book.authors or '',
                    book.publisher or '',
                    book.year or ''
                ])
    print(f"Exported {len(books)} books to {CSV_FILE}")


# Import Book records from CSV
def import_books_from_csv(csv_file=CSV_FILE):
    with app.app_context():
        db.create_all()
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


if __name__ == "__main__":
    # Uncomment the function you want to run
    # export_books_to_csv()
    import_books_from_csv()
    pass
