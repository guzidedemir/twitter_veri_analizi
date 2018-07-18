import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentimentAnalysis:

    def __init__(self, searchTerm, noOfTerms):
        self.searchTerm = searchTerm
        self.noOfTerms = noOfTerms
        self.tweets = []
        self.tweetText = []

    def downloadData(self):
        # authenticating
        consumerKey ="Z4IEpFGELpwESUBMREmrCo8bk"
        consumerSecret ="IO21mAJ7va62eEIEuVaNpeRBxXDSQMI4kewtRtmX4lc3uoSCcu"
        accessToken ="57120624-RkSaTDzrhLsRRNzQWm13Col4Pbfa8ocmGV5j6gfXv"
        accessTokenSecret = "ndfTXDJ0qFxTUXk8QgzYmExUm7TQI52B6U2aUwRyFjB78"
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        # searchTerm = input("Aranacak kelime/hashtag yazınız: ")
        # NoOfTerms = int(input("Kaç tweet arasından analiz edilsin: "))








        # searching for tweets
        self.tweets = tweepy.Cursor(api.search,q=self.searchTerm, lang = "tr").items(self.noOfTerms)## ingilizce tivitleri alıyor.

        #Biz türkçe alacağız ingilizceye çevireceğiz ingilizce üzerinden analiz yapacağız
       ## self.tweets= api.user_timeline(screen_name="recepaliskan")


        # Open/create a file to append data to
        # csvFile = open('result.csv', 'a')

        # Use csv writer
        # csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        stream = [["Kullanıcı", "Pozitiflik"]]

        sayac=0
        # iterating through tweets fetched
        for tweet in self.tweets:

            sayac+=1
            # print(sayac, ": ", tweet.text )
            #print(tweet.text)

            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            try:
                analysis = TextBlob(tweet.text).translate(from_lang="tr", to='en')##türkçeden ingilizceye çevirdik
            except:
                analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
            stream.append([tweet.user.screen_name, polarity])
            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1
            #print(analysis)

        # Write to csv and close csv file
       # csvWriter.writerow(analysis)
       #  csvWriter.writerow(self.tweetText)
       #  csvFile.close()

        # finding average of how people are reacting
        # positive = self.percentage(positive, self.noOfTerms)
        # wpositive = self.percentage(wpositive, self.noOfTerms)
        # spositive = self.percentage(spositive, self.noOfTerms)
        # negative = self.percentage(negative, self.noOfTerms)
        # wnegative = self.percentage(wnegative, self.noOfTerms)
        # snegative = self.percentage(snegative, self.noOfTerms)
        # neutral = self.percentage(neutral, self.noOfTerms)

        # finding average reaction
        polarity = polarity / self.noOfTerms

        # printing out data
        # print("Kişilerin " + self.searchTerm + " analizinde " + str(self.noOfTerms) + " tweetleri.")
        # print()
        # print("General Report: ")
        #
        # if (polarity == 0):
        #     print("Neutral")
        # elif (polarity > 0 and polarity <= 0.3):
        #     print("Weakly Positive")
        # elif (polarity > 0.3 and polarity <= 0.6):
        #     print("Positive")
        # elif (polarity > 0.6 and polarity <= 1):
        #     print("Strongly Positive")
        # elif (polarity > -0.3 and polarity <= 0):
        #     print("Weakly Negative")
        # elif (polarity > -0.6 and polarity <= -0.3):
        #     print("Negative")
        # elif (polarity > -1 and polarity <= -0.6):
        #     print("Strongly Negative")

        # print()
        # print("Detailed Report: ")
        # print(str(positive) + "% people thought it was positive")
        # print(str(wpositive) + "% people thought it was weakly positive")
        # print(str(spositive) + "% people thought it was strongly positive")
        # print(str(negative) + "% people thought it was negative")
        # print(str(wnegative) + "% people thought it was weakly negative")
        # print(str(snegative) + "% people thought it was strongly negative")
        # print(str(neutral) + "% people thought it was neutral")

        categorical = [["Kategori", "Twit Sayısı"],
                       ["Çok Olumlu", spositive],
                       ["Olumlu", positive],
                       ["Kısmen Olumlu", wpositive],
                       ["Nötr", neutral],
                       ["Kısmen Olumsuz", wnegative],
                       ["Olumsuz", negative],
                       ["Aşırı Olumsuz", snegative]]

        # self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, self.searchTerm, self.noOfTerms)

        return "\n\n----------\n\n".join(self.tweetText), categorical, stream


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis("test", 25)
    print(sa.downloadData())
