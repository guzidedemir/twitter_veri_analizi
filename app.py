from flask import Flask, render_template, request
from tweet import SentimentAnalysis

app = Flask(__name__)


@app.route('/')
def hello_world(word=None):
    # http://localhost:5000/

    if word is None:
        word = "default"
        description = "İstediğiniz kelimeleri içeren tweetleri analiz edin!"
    else:
        description = "Aranan kelime: {}".format(word)

    tweet_data, chart_data, graph_data = SentimentAnalysis(word, 25).downloadData()

    # Data Sample:
    # tweet_data = "Twit 1\nTwit 2\nTwit 3"
    # chart_data = [['Category', 'Amount'], ['Positive', 8], ['Negative', 2]]
    # graph_data = [['Time', 'Sentiment'], ["10:54", 0.7], ["11:22", 0.5]]

    return render_template("content.html", desc=description, tweet=tweet_data, chart=chart_data, graph=graph_data)


@app.route('/search_tweet', methods=['POST'])
def search_tweet():
    search_word = request.form["search_input"]
    return hello_world(search_word)


if __name__ == '__main__':
    app.run()
