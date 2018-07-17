from flask import Flask, render_template
from flask import Flask
from flask import Markup
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    # It runs on http://localhost:5000/
    return render_template("test.html")




if __name__ == '__main__':
    app.run()
