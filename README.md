# OLP Library Data

This project provides a simple library database for students to practice integrating book data into their own projects. It uses ISBNs to fetch book metadata and store it in a database.

## Main Tools and Scripts

- **populate_books.py**: Reads ISBNs from `isbn.txt`, validates them, fetches book metadata from Open Library using the `isbnlib` library, and populates the database with Book records. It can be run in test mode to process only a few books for quick testing.

- **models.py**: Defines the Book model and database structure using SQLAlchemy. The Book class can be created with just an ISBN, and it will automatically fetch and fill in the rest of the metadata.

- **csv_utils.py**: Provides functions to export all Book records to a CSV file and import Book records from a CSV file. This makes it easy for students to work with the data in a beginner-friendly format.

## How It Works

1. Add ISBNs to `isbn.txt` (one per line).
2. Run `populate_books.py` to build the database from ISBNs.
3. Use `csv_utils.py` to export/import data as CSV for easy sharing and integration.

## Requirements

Install dependencies with:

```
pip install -r requirements.txt
```

## For Students

You can use the CSV export to integrate book data into your own projects, rebuild the database, or practice importing records. The Book model is designed to be easy to use and extend.

