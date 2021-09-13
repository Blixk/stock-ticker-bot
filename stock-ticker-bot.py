import os
import tweepy
import logging
import time
import json
# import argparse
# not adding in arguments yet -- future state will let user select batch or
# streaming tweet collection via cli arguments 

from datetime import datetime, date, timedelta
from google.cloud import storage


cashtag = os.environ['CASHTAG']


# scrape cashtag for last day's tweets
def cashtag_scrape():
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    today = date.today()
    delta = timedelta(days=1)


    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    tweet_list = []
    for tweet in tweepy.Cursor(api.search, q=cashtag, lang="en", since=today-delta, until=today, tweet_mode="extended").items():
        tweet_model = {}
        tweet_model['tweet_id'] = tweet.id
        tweet_model['tweet_cashtag'] = cashtag.strip('\\\\')
        tweet_model['tweet_text'] = tweet.full_text
        tweet_model['tweet_response_to_userid'] = tweet.in_reply_to_user_id
        tweet_model['tweet_timestamp'] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
        tweet_model['tweet_favorite_count'] = tweet.favorite_count
        tweet_model['tweet_retweet_count'] = tweet.retweet_count
        tweet_model['tweet_author_id'] = tweet.user.id
        tweet_model['tweet_author_followers'] = tweet.user.followers_count
        tweet_model['tweet_author_location'] = tweet.user.location
        tweet_model['tweet_author_creation_date'] = tweet.user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        print(tweet_model)
        tweet_list.append(tweet_model)
    return tweet_list
        

def write_tweets_to_storage(tweet_list):
    gcp_credentials = os.environ['GCP_CREDENTIALS']
    bucket_name = os.environ['GCP_BUCKET_NAME']
    for tweet in tweet_list:
        filename = str(time.time()) + '-' + cashtag.strip('\\$') + '-tweet.json'
        client = storage.Client.from_service_account_json(gcp_credentials)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(filename)
        with open(filename, 'w') as fp:
            json.dump(tweet, fp, indent=4)
        fp.close()
        blob.upload_from_filename(filename)
        os.remove(filename)

def main():
    tweets = cashtag_scrape()
    write_tweets_to_storage(tweets)

if __name__ == "__main__":
    main()
