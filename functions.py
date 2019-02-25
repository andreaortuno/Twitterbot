import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk import word_tokenize
import re
import os
import datetime
import pickle
import tweepy
import warnings

from os import path
from wordcloud import WordCloud
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from nltk.data import load

from sklearn.neural_network import MLPClassifier

warnings.filterwarnings("ignore")

tagdict = load('help/tagsets/upenn_tagset.pickle')
nlp_keys = tagdict.keys()

def cleanupdata(tweet, date):
    #function to get the avg number of words of each sentence
    def avg_word(sentence):
        words = sentence.split()
        if len(words) == 0:
            return 0
        return (sum(len(word) for word in words)/len(words))


    #define_individual features
    tweets_text = [] #raw tweet text without links, hashtags, or mentions
    mentions = [] # number of mentions
    links = [] # number of links in tweet
    hashtags = [] # number of hashtags in tweet
    basic_features = [] # [num_words, num_char, avg_word_len, num_stopwords, num_schar, num_numerics, num_uppercase]
    nlp_tags_frequency = [] # tags frequency provided by the NLP
    time = [] # time of day the tweet was published

    stop = stopwords.words('english')

    #feature extraction
    nlp_dict = {key: 0 for key in nlp_keys}
    frequency = np.zeros((1, len(nlp_keys)))
    tweets_text = re.sub("[^a-zA-Z0-9]", " ", (re.sub('https?://[A-Za-z0-9./]+','',
                                                               re.sub(r'@[A-Za-z0-9]+','', tweet)))).lower()
    mentions = len(re.findall('@[A-Za-z0-9]+', tweet))
    links = float(re.findall('https?://[A-Za-z0-9./]+', tweet) != [])
    hashtags = len(re.findall('#[A-Za-z0-9./]+', tweet))

    try:
        time.append(date.hour)
    except:
        time.append(date.hour)

    text = re.sub("[^a-zA-Z0-9 ]", "", (re.sub('https?://[A-Za-z0-9./]+' or "[^a-zA-Z0-9]",'', tweet)))
    text = text.replace('  ', '')
    if text != '' and text[-1] == ' ':
        text = text[:-1]

    num_words = lambda x: len(str(x).split(" "))
    avg_word_len = lambda x: avg_word(x)
    num_stopwords = lambda x: len([x for x in x.split() if x in stop])
    num_numerics = lambda x: len([x for x in x.split() if x.isdigit()])
    num_upper = lambda x: len([x for x in x.split() if x.isupper()])


    basic_features.append([num_words(text), len(text), avg_word_len(text), num_stopwords(text),
                      len(re.findall('#[A-Za-z0-9./]+', tweet)), num_numerics(text),
                           num_upper(text)])
    for word, tag in nltk.pos_tag(word_tokenize(re.sub('#', '',tweet))):
        nlp_dict[tag] += 1


    k=0
    for key in nlp_dict:
        frequency[0][k] = nlp_dict[key]
        k +=1
    nlp_tags_frequency.append(frequency)


    X_features=[]
        # puts all features for a tweet in a numpy array
    arr = np.concatenate([np.array([mentions, links, hashtags]), np.array(basic_features[0])])
    arr = np.concatenate([arr,  nlp_tags_frequency[0][0]])
    arr = np.concatenate([arr,  time])
    X_features = arr

    return X_features

#check if the user made the tweet
def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

#gets prediction from the new tweet
def get_prediction(text, date):

    x_Tweet = cleanupdata(text, date)
    loaded_model = pickle.load(open('mlpsave.sav', 'rb'))
    prediction = loaded_model.predict([x_Tweet])
    if prediction == 1:
        return True
    else:
        return False
