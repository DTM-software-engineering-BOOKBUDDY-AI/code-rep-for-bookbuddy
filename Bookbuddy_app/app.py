from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, UserMixin, current_user # type: ignore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with a real secret key
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    return None  # For now, return None as we don't have user authentication yet

@app.route('/')
@app.route('/home')
def hello_world():
    return render_template("homepage.html")

@app.route('/form' )
def form():
    return render_template("form page/form.html")

@app.route('/recommendation')
def recommendation():
    # Create a sample book object (later this would come from your database)
    book = {
        'id': 1,
        'title': "Don Quixote",
        'author': "Miguel de Cervantes",
        'cover': "https://covers.openlibrary.org/b/id/8224816-L.jpg",
        'rating': "4.5",
        'genre': "Novel",
        'language': "Spanish",
        'year': "1605",
        'summary': "Don Quixote is a Spanish novel that follows the adventures of a noble who, after reading too many chivalric romances, loses his sanity...",
        'fullSummary': "The story tells the adventures of a nobleman who reads so many chivalric romances that he loses his mind and decides to become a knight-errant, recruiting a simple farmer, Sancho Panza, as his squire..."
    }
    return render_template("recommendation.html", book=book)

@app.route('/testbase')
def testbase():
    return render_template("testing_base.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/book/details/<int:book_id>')
def book_details(book_id):
    # Add your logic to fetch book details
    return render_template('book_details.html', book_id=book_id)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/my_lib')
def my_lib():
    # Sample book collections
    library_books = {
        'current_books': [
            {
                'id': 1,
                'title': "The Alchemist",
                'author': "Paulo Coelho",
                'progress': 45,
                'image': "01.jpg"
            },
            {
                'id': 2,
                'title': "Dune",
                'author': "Frank Herbert",
                'progress': 30,
                'image': "02.jpg"
            },
            {
                'id': 3,
                'title': "1984",
                'author': "George Orwell",
                'progress': 75,
                'image': "03.jpg"
            }
        ],
        'want_to_read': [
            {
                'id': 4,
                'title': "The Midnight Library",
                'author': "Matt Haig",
                'image': "04.jpg"
            },
            {
                'id': 5,
                'title': "Project Hail Mary",
                'author': "Andy Weir",
                'image': "05.jpg"
            },
            {
                'id': 6,
                'title': "The Seven Husbands of Evelyn Hugo",
                'author': "Taylor Jenkins Reid",
                'image': "06.jpg"
            }
        ],
        'finished_books': [
            {
                'id': 7,
                'title': "The Thursday Murder Club",
                'author': "Richard Osman",
                'image': "07.jpg"
            },
            {
                'id': 8,
                'title': "Klara and the Sun",
                'author': "Kazuo Ishiguro",
                'image': "08.jpg"
            },
            {
                'id': 9,
                'title': "The Invisible Life of Addie LaRue",
                'author': "V.E. Schwab",
                'image': "09.jpg"
            }
        ]
    }
    return render_template('my_lib.html', books=library_books)

if __name__ == '__main__':
    app.run(debug=True)