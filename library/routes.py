from flask import (render_template, url_for, flash, redirect, request)
from library import app, db
from library.forms import AddBookForm, EditMemberForm, AddMemberForm, IssueBookForm, ReturnBookForm, SearchBookForm
from library.models import User, Book, BookIssuance
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
    

@app.route("/about")
def about():
    return render_template('about.html', title='About')

#view members
@app.route("/members")
def members():
    users = User.query.all()
    return render_template('members.html', title='Members', users=users)

#view member
@app.route("/member_item/<int:user_id>")
def member_item(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('member_item.html', user=user)

#add member
@app.route("/members/new", methods=['GET', 'POST'])
def add_member():
     # Get form data from request
    form = AddMemberForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash('New member added successfully!', 'success')
        return redirect(url_for('members'))

    # To handle GET request to route    
    return render_template('add_member.html', form=form)

#update member
@app.route("/members/<int:user_id>/update", methods=['GET', 'POST'])
def edit_member(user_id):
    user = User.query.get_or_404(user_id)
    form = EditMemberForm()

    #to update member values
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.amount_due = form.amount_due.data
        db.session.commit()
        flash('Member updated successfully!', 'success')
        return redirect(url_for('members', user_id=user.id))

    #to get initial values of member    
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.amount_due.data = user.amount_due

    #to handle GET request to route
    form.submit.label.text = "Update"
    return render_template('edit_member.html', 
                           form=form, legend='Update Member')

#delete member
@app.route("/members/<int:user_id>/delete", methods=['POST'])
def delete_member(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('The member has been deleted!', 'success')
    return redirect(url_for('members'))


#books
@app.route("/books")
def books():
    books = Book.query.all()
    return render_template('books.html', title='Books', books=books)

#book detail
@app.route("/book_item/<int:book_id>")
def book_item(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_item.html', book=book)

#add book
@app.route("/books/new", methods=['GET', 'POST'])
def add_book():
     # Get form data from request
    form = AddBookForm()
    if form.validate_on_submit():
        new_book = Book(title=form.title.data, author=form.author.data, isbn=form.isbn.data, num_pages=form.num_pages.data, text_reviews_count=form.text_reviews_count.data, date_published=form.date_published.data, publisher=form.publisher.data, total_quantity=form.total_quantity.data)
        db.session.add(new_book)
        db.session.commit()
        flash('New book added successfully!', 'success')
        return redirect(url_for('books'))

    # To handle GET request to route    
    return render_template('add_book.html', form=form)

# Edit Book
@app.route("/books/<int:book_id>/update", methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = AddBookForm()

    #to update book values
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.num_pages = form.num_pages.data
        book.text_reviews_count = form.text_reviews_count.data
        book.date_published = form.date_published.data
        book.publisher = form.publisher.data
        book.total_quantity = form.total_quantity.data
        db.session.commit()
        flash('Your book has been updated!', 'success')
        return redirect(url_for('book_item', book_id=book.id))

    #to get initial values of book    
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.isbn.data = book.isbn
        form.num_pages.data = book.num_pages
        form.text_reviews_count.data = book.text_reviews_count
        form.date_published.data = book.date_published
        form.publisher.data = book.publisher
        form.total_quantity.data = book.total_quantity

    form.submit.label.text = "Update"
    #to handle GET request to route
    return render_template('edit_book.html', title='Edit Book',
                           form=form)

#delete book
@app.route("/books/<int:book_id>/delete", methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Your book has been deleted!', 'success')
    return redirect(url_for('books'))


#issue book
@app.route("/issue_book/<int:book_id>", methods=['GET', 'POST'])
def issue_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = IssueBookForm()
    

    if form.validate_on_submit():
 
        #check available quantity
        if book.total_quantity >= 1:

            issuance = BookIssuance(user_id=form.user_id.data, username=form.username.data, book_id=form.book_id.data, title=form.title.data, author=form.author.data, date_issued=form.date_issued.data, due_date=form.due_date.data, per_day_fee=form.per_day_fee.data)

            #update book availability status
            book.total_quantity -= 1
            db.session.add(issuance)
            db.session.commit()

            flash('Book issued successfully', 'success')
            return redirect(url_for('books'))
        else:
            flash('Book is not available to issue', 'danger')

    elif request.method == 'GET':
        form.book_id.data = book.id
        form.title.data = book.title
        form.author.data = book.author

    #to handle GET request to route
    return render_template('issue_book.html', form=form)


#return book
@app.route('/return_book/<int:transaction_id>', methods=['GET', 'POST'])
def return_book(transaction_id):
    # Get the BookIssuance record based on the transaction_id
    book_issuance = BookIssuance.query.get_or_404(transaction_id)
    form = ReturnBookForm()
     # Calculate total charge
    return_date = datetime.now().date()
    difference = return_date - book_issuance.date_issued
    difference = difference.days
    total_charge = difference * book_issuance.per_day_fee

    if request.method == 'POST':

        # Calculate debt for this transaction based on amount_paid
        amount_paid = float(form.amount_paid.data)
        transaction_debt = total_charge - amount_paid

        # Check if amount_due + transaction_debt exceeds ksh 500
        user = book_issuance.user
        amount_due = user.amount_due
        if(amount_due + transaction_debt > 500):
            flash('Outstanding Debt Cannot Exceed Ksh.500', 'danger')
            return render_template('return_book.html', form=form, total_charge=total_charge, difference=difference, book_issuance=book_issuance)

        #update user amount_due
        if transaction_debt:
            user.amount_due += transaction_debt

        # Update the book issuance record
        book_issuance.return_date = return_date
        book_issuance.returned = True
        #update book availability
        book = book_issuance.book
        book.total_quantity += 1
        db.session.commit()
        flash('Book returned successfully', 'success')
        return redirect(url_for('transactions'))


    # To handle GET request to route
    return render_template('return_book.html', form=form, total_charge=total_charge, difference=difference, book_issuance=book_issuance) 


#transactions
@app.route("/transactions")
def transactions():
    transactions = BookIssuance.query.all()
    return render_template('transactions.html', transactions=transactions)

#reports
@app.route("/reports")
def reports():
    most_reviewed_books = Book.query.order_by(Book.text_reviews_count.desc()).all()
    users = User.query.order_by(User.amount_due.desc()).all()

    return render_template('reports.html', books=most_reviewed_books, users=users)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchBookForm()
    title = form.title.data
    author = form.author.data

    if form.validate_on_submit():

        # Query the database for books based on the search criteria
        if title and author:
            # Search by both book title and author
            books = Book.query.filter(Book.title.ilike(f'%{title}%'), Book.author.ilike(f'%{author}%')).all()
            if books:
                flash('Results Found', 'success')
                return render_template('search_book.html', books=books, form=form)
            else:
                flash('No Results Found', 'danger')
        elif title:
            # Search by book title only
            books = Book.query.filter(Book.title.ilike(f'%{title}%')).all()
            if books:
                flash('Results Found', 'success')
                return render_template('search_book.html', books=books, form=form)
            else:
                flash('No Results Found', 'danger')
        elif author:
            # Search by author only
            books = Book.query.filter(Book.author.ilike(f'%{author}%')).all()
            if books:
                flash('Results Found', 'success')
                return render_template('search_book.html', books=books, form=form)
            else:
                flash('No Results Found', 'danger')
        else:
            # No search criteria provided
            books = []
            return render_template('search_book.html', books=books)

    # To handle GET request to route
    return render_template('search_book.html', form=form)