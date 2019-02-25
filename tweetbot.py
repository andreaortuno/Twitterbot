import tweepy
from secrets import * #this file contains the twitter Keys the bot uses
from functions import *

#create an OAuthHandler instance
# Twitter requires all requests to use OAuth for authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_secret)

 #Construct the API instance
global api
api = tweepy.API(auth) # create an API object

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        #check if the tweet is from the person we are following
        if from_creator(status):
            try:
                #print(status.extended_tweet['full_text'])
                text = status.extended_tweet['full_text']
            except:
                #print(status.text)
                text = status.text

            date = status.created_at
            id = status.id

            prediction = get_prediction(text, date)

            if prediction:
                #print("I predict that this tweet is directly from Trump")
                updated_status = "I predict that this tweet is directly from Trump  " + datetime.datetime.now().strftime("%H:%M:%S")
            else:
                #print("I predict that this tweet was written by Trump's staff")
                updated_status = "I predict that this tweet was written by Trump's staff  " + datetime.datetime.now().strftime("%H:%M:%S")

            #api.update_status(status=updated_status)

            #post on the prediction on the account
            reply_status = "@%s %s  " % ("realDonaldTrump", updated_status)
            api.update_status(status=reply_status, in_reply_to_status_id=id, auto_populate_reply_metadata=True)
            return True
        return True

#call on stream listener
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode='extended')

myStream.filter(follow=['25073877'])
