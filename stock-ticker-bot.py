import os
import tweepy

from datetime import date, timedelta
from google.cloud import storage

# scrape cashtag for last day's tweets
def cashtag_scrape():
    cashtag = os.environ['CASHTAG']
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    today = date.today()
    delta = timedelta(days=1)
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth_handler=auth)
    for raw_tweet in tweepy.Cursor(api.search, q=cashtag, lang="en", since=today-delta, until=today).items():
        pass # need to build model, so do nothing for now

def write_tweets_to_storage():
    pass # WIP


def main():
    cashtag_scrape()


if __name__ == "__main__":
    main()
