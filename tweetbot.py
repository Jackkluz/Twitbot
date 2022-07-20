import time
import os

import tweepy
from dotenv import load_dotenv

load_dotenv()

T_API_KEY = os.getenv('twitter_api_key')
T_API_SECRET = os.getenv('twitter_api_secret')
T_TOKEN = os.getenv('twitter_token')
T_TOKEN_SECRET = os.getenv('twitter_token_secret')

auth = tweepy.OAuthHandler(T_API_KEY, T_API_SECRET)
auth.set_access_token(T_TOKEN, T_TOKEN_SECRET)


api = tweepy.API(auth)


def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        time.sleep(300)


user = api.me()   # or user = api.get_user(screen_name="myTwitterUserName")
print(user.followers_count)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)


def follow_back(num_followers):
    # follow back if follows you and has x number of followers
    for follower in limit_handler(tweepy.Cursor(api.followers).items()):
        if follower.followers_counter > int(num_followers):
            follower.follow()
            break


# input follower with ''
# follow_back()


def liker(keyword):
    # autolike tweets with keyword
    search_string = keyword
    numbersofTweets = 5
    for tweet in tweepy.Cursor(api.search, search_string).items(numbersofTweets):
        try:
            tweet.favorite()
            # tweet.retweet()
            print('I liked that tweet')
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

# search keyword with ''
# liker()
