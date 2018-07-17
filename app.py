from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    # http://localhost:5000/
    return render_template("content.html")


@app.route('/search_word')
def search_word():
    print("Test")
    return ""


if __name__ == '__main__':
    app.run()
