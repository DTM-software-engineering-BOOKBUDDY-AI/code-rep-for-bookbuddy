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

if __name__ == '__main__':
    app.run(debug=True)