from flask_wtf import FlaskForm
from wtforms import validators, StringField, IntegerField, PasswordField, DateField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class AddBookForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=2, max=255)])
    author = StringField('Author(s)', [validators.Length(min=2, max=255)])
    isbn = StringField('ISBN', [validators.Length(min=10, max=10)])
    num_pages = IntegerField('No. of Pages', [validators.NumberRange(min=1)])
    text_reviews_count = IntegerField('No. of Text Reviews', [validators.NumberRange(min=0)])
    date_published = DateField('Publication Date', [validators.InputRequired()])
    publisher = StringField('Publisher', [validators.Length(min=2, max=255)])
    total_quantity = IntegerField('Total No. of Books', [validators.NumberRange(min=1)])
    submit = SubmitField('Add')


class AddMemberForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Add')

class EditMemberForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    amount_due = StringField('Amount Due (Ksh)', [validators.Length(min=1, max=11)])
    submit = SubmitField('Add')


class IssueBookForm(FlaskForm):
    user_id = StringField('Member ID', [validators.Length(min=1, max=11)])
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=2, max=20)])
    book_id = StringField('Book ID', [validators.Length(min=1, max=11)])
    title = StringField('Book Title', [validators.Length(min=2, max=255)])
    author = StringField('Book Author(s)', [validators.Length(min=2, max=255)])
    date_issued = DateField('Issue Date', [validators.InputRequired()])
    due_date = DateField('Due Date', [validators.InputRequired()])
    per_day_fee = StringField('Per Day Fee (Ksh)', [validators.Length(min=1, max=11)])
    submit = SubmitField('Submit')

class ReturnBookForm(FlaskForm):
    amount_paid = StringField('Amount Paid (Ksh)', [validators.Length(min=1, max=11)])
    submit = SubmitField('Return')

class SearchBookForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=0, max=255)])
    author = StringField('Author(s)', [validators.Length(min=0, max=255)])
    submit = SubmitField('Search')