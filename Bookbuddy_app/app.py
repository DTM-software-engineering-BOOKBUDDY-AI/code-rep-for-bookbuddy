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
    return render_template("recommendation.html")

@app.route('/testbase')
def testbase():
    return render_template("testing_base.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)