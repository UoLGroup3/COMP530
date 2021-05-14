from flask import Flask,render_template, redirect, request
import numpy as np
import tweepy 
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import re

app = Flask(__name__)

@app.route('/sentiment', methods = ['GET','POST'])
def sentiment():
    userid = ""
 
    hashtag = request.form.get('hashtag')
    error="Error"
    render_template('index.html', error=error)

    

    consumerKey="1p433aDX9parHh2l4TUPn8p4X"

    consumerSecret="zwnMrqo2h0eZRWIlKczSkiuZNZSCpPEyDr5MepI9qt9hliRroN"

    accessToken="2242617514-pvs6vWpyOH3nD594Ta7A5afUU57iQCfoYNOq3wg"

    accessTokenSecret="VjPhYpMj9KKylvMcrveBbjYhEmS91fVSJlJWsHMwrZdCu"

 
    
    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
    authenticate.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(authenticate, wait_on_rate_limit = True)

    def cleanTxt(text):
        text = re.sub('@[A-Za-z0–9]+', '', text) 
        text = re.sub('#', '', text)
        text = re.sub('RT[\s]+', '', text) 
        text = re.sub('https?:\/\/\S+', '', text)
        return text
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity
    def getAnalysis(score):
            if score < 0:
                return 'Negative'
            elif score == 0:
                return 'Neutral'
            else:
                return 'Positive'

    if userid == "":
        # hash tag coding
        m = []
        m1 =[]
        for tweet in tweepy.Cursor(api.search, q=hashtag).items(500):
            m1 = [tweet.text] 
            m1 = tuple(m1)                    
            m.append(m1)

        df = pd.DataFrame(m)
        df['Tweets'] = df[0].apply(cleanTxt)
        df.drop(0, axis=1, inplace=True)
        df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
        df['Polarity'] = df['Tweets'].apply(getPolarity)
        df['Analysis'] = df['Polarity'].apply(getAnalysis)
        positive = df.loc[df['Analysis'].str.contains('Positive')]
        negative = df.loc[df['Analysis'].str.contains('Negative')]
        neutral = df.loc[df['Analysis'].str.contains('Neutral')]

        positive_per = round((positive.shape[0]/df.shape[0])*100, 1)
        negative_per = round((negative.shape[0]/df.shape[0])*100, 1)
        neutral_per = round((neutral.shape[0]/df.shape[0])*100, 1)

        return render_template('sentiment.html', name=hashtag,positive=positive_per,negative=negative_per,neutral=neutral_per)
   
@app.route('/')
def home():
    return render_template('index.html')

app.run(debug=True)
