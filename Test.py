import os

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/<sportshome>")
def home(sportshome):
    return render_template("sportshome.html")


@app.route("/<sportsavatar>")
def avatar():
    return render_template("sportsavatar.html")


if __name__ == "__main__":
    app.run(debug=True)
