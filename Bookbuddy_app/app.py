from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)
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
if __name__ == '__main__':
    app.run(debug=True)