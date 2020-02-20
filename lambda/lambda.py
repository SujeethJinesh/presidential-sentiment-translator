# Modified from https://gist.github.com/yanofsky/5436496
import csv

from models.candidate import Candidate
from models.party_affiliation import PartyAffiliation
from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
from .models.candidate_tweet import CandidateTweet

import tweepy

candidates = [Candidate("Andrew Yang", "AndrewYang", PartyAffiliation.democrat)]


def authorize_tweepy():
    '''
    authorize twitter, initialize tweepy
    :return: authorized api
    '''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    return api


def analyze_sentiment(text):
    pass


def get_all_tweets(tweepy, candidate):
    '''
    Twitter only allows access to a users most recent 3240 tweets with this method
    :param tweepy: api we'll be using to get tweets
    :param screen_name: candidate's twitter_handle we'll be using to scrape
    :return: list of tweets for the candidate
    '''
    # initialize a list to hold all the tweepy Tweets
    all_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = tweepy.user_timeline(screen_name=candidate.twitter_handle, count=200)

    # save most recent tweets
    all_tweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % oldest)

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = tweepy.user_timeline(screen_name=candidate.twitter_handle, count=200, max_id=oldest)

        # save most recent tweets
        all_tweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(all_tweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    
    out_tweets = [CandidateTweet(candidate, tweet.text.encode("utf-8"), tweet.id_str,
                                 analyze_sentiment(tweet.text)) for tweet in all_tweets]
    
    return out_tweets
    
    # write the csv
    # with open('%s_tweets.csv' % candidate.twitter_handle, 'r') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["id", "created_at", "text"])
    #     writer.writerows(out_tweets)
    # pass


if __name__ == '__main__':
    api = authorize_tweepy()
    
    for curr_candidate in candidates:
        get_all_tweets(api, curr_candidate)
