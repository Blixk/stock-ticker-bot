import twitter
import os
import requests

from google.cloud import storage


#det GET 'https://api.twitter.com/2/tweets/search/all?query=(covid%20OR%20coronavirus)&max_results=500' --header 'Authorization: Bearer $BEARER_TOKEN'

def scrape():
    twitter_bearer_token = os.environ['TWITTER_BEARER_TOKEN']
    headers = {}
    headers["Authorization"] = "Bearer " + twitter_bearer_token
    r = requests.get("https://api.twitter.com/2/tweets/search/all?query=(GOOGL)&max_results=20", headers=headers)
    print(r.text)


def main():
    scrape()


if __name__ == "__main__":
    main()
