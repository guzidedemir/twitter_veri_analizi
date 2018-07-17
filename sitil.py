from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def chart():


if __name__ == "__main__":
    app.run()