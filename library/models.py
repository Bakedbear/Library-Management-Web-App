from datetime import datetime, date
from library import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), unique=False, nullable=False)
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    num_pages = db.Column(db.Integer, unique=False, nullable=False)
    text_reviews_count = db.Column(db.Integer, unique=False, nullable=False)
    date_published = db.Column(db.Date, unique=False, nullable=False)
    publisher = db.Column(db.String(100), unique=False, nullable=False)
    total_quantity = db.Column(db.Integer, unique=False, nullable=False)
    
    def __repr__(self):
        return f"Book('{self.id}', '{self.title}', '{self.author}', '{self.num_pages}', '{self.publisher}', '{self.date_published}, '{self.total_quantity}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.Date, unique=False, default=datetime.utcnow)
    amount_due = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.date_created}', '{self.amount_due}')"


class BookIssuance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(20), unique=False, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    title = db.Column(db.String(100), unique=False, nullable=False)
    author = db.Column(db.String(100), unique=False, nullable=False)
    date_issued = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    returned = db.Column(db.Boolean, default=False)
    per_day_fee = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"BookIssuance('{self.id}', '{self.username}', '{self.title}', '{self.author}', '{self.date_issued}', '{self.due_date}', '{self.per_day_fee}')"

    #relationships to the User and Book models
    user = db.relationship('User', backref='book_issuances')
    book = db.relationship('Book', backref='book_issuances')