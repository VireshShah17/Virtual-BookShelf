# Database and Backend management using SQLite3, SQLAlchemy and Flask
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Creating the flask app
app = Flask(__name__)
# Creating the database to store the record
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Creating a table
with app.app_context():
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(150), nullable=False, unique=True)
        author = db.Column(db.String(150), nullable=False)
        rating = db.Column(db.Float, nullable=False)
    db.create_all()


# Function to render the home page of our website
@app.route('/')
def home():
    # Fetching all the record from the database
    all_books = db.session.query(Book).all()
    # rendering the home page and book details of user entered
    return render_template('index.html', books=all_books)


# Function to render the add page of our website
@app.route("/add", methods=["GET", "POST"])
def add():
    # getting the book request from the user
    if request.method == "POST":
        with app.app_context():
            new_book = Book(
                title = request.form['book_name'],
                author = request.form['book_author'],
                rating = request.form['book_rating']
            )
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


# Function to render edit rating page of the website
@app.route('/edit', methods=['GET', 'POST'])
def edit_rating():
    if request.method == 'POST':
        with app.app_context():
            # Updating the record
            book_id = request.form['id']
            book_to_update = Book.query.get(book_id)
            book_to_update.rating = request.form["newRating"]
            db.session.commit()
            return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template('edit.html', book=book_selected)


# Function to delete a record from the website
@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    # Deleting the record
    with app.app_context():
        book_to_delete = Book.query.get(book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

