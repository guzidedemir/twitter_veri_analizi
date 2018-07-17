from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    # http://localhost:5000/
    return render_template("content.html")


if __name__ == '__main__':
    app.run()
