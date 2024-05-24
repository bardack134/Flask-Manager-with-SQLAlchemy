from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

# Create an instance of the Flask application
app = Flask(__name__)

# Configure the Flask application to use a SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'

# Create a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Create an instance of SQLAlchemy using the custom base class
db = SQLAlchemy(model_class=Base)

# Initialize the app with the SQLAlchemy extension
db.init_app(app)

# Define the database model for the books table
class Book(db.Model):
    # Define the columns of the table
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float(), unique=False, nullable=False)

    # Initializer for the Book class
    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating

# Create the table schema in the database. This requires the application context.
with app.app_context():
    db.create_all()

# Insert a new record into the books table
with app.app_context():
    new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)
    db.session.commit()

# Read all records from the books table
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
    print(result)

# Read a particular record by query
with app.app_context():
    book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    print(book)

# Read a particular record using `filter_by`
with app.app_context():
    book = db.session.execute(db.select(Book).filter_by(title='Harry Potter')).scalar_one()
    print(book)

# Update a particular record by query
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    book_to_update.title = "Harry Potter and the Chamber of Secrets"
    db.session.commit()

# Update a record by primary key
book_id = 1
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    book_to_update.title = "Harry Potter and the Goblet of Fire"
    db.session.commit()

# Delete a record by primary key
book_id = 1
with app.app_context():
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
