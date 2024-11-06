from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)
@app.route('/')
@app.route('/home')
def hello_world():
    return render_template("/home/homepage.html")

@app.route('/Recomendation_page')
def Recomendation_page():
    return render_template("/recom page/Recomendation_page.html")

app.run(debug=True)
