# Is it Trump? Tweetbot

Using Machine Learning to predict if a tweet sent by the 45th president's twitter account is from the president or from his staff. In 2016 it was hypothesized that President Trump tweeted only from his android phone and his staff tweeted from his account using an iphone. This was addressed by their administration already and now all the tweets are sent from iphones. This project was done using the scikit-learn library and Python.

## How it works:

Because in 2015-2016 the presidential account posted tweets from two different phones, an android phone and an i-phone we were able to obtain a data set of tweets that might have been written by Trump himself and others that might have been written by his staff. [Here](http://varianceexplained.org/r/trump-tweets/) is a link of some data analysis that was performend on this data set to confirm this theory. Since then the account has been changed to only publish from an iphone. 

Using the data set and scikit-learn we trained a ML classifier to predict if a tweet came from the president directly or from his staff. In this code we use the trained classifier to predict if a new tweet from Donald Trump's account is written directly by him or his staff. The new tweets are read using tweepy and processed using NLP and some data cleaning before they using the ML model. After the model makes its prediction, the prediction is posted as a reply tweet.

You can see the twitter account [here](https://twitter.com/IsItTrump1). 
