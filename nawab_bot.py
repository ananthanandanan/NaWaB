#!/usr/bin/env python2

import json
import config
import tweepy
import mmap
import time
import random

def nawab_twitter_authenticate():
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token_key, config.access_token_secret)
    api = tweepy.API(auth)
    return api

def nawab_read_list():
    proto_list = open('protobuf_list.txt', 'r')
    search_term = proto_list.readlines()
    return search_term

def nawab_store_id(tweet_id):
    ### Store a tweet id in a file
    with open("tid_store.txt","a") as fp:
        fp.write(str(tweet_id) + str('\n'))

def nawab_get_id():
    ### Read the last retweeted id from a file
    with open("tid_store.txt", "r") as fp:
        for line in fp:
            return line

def nawab_check_tweet(tweet_id):
    with open("tid_store.txt", "r") as fp:
        for line in fp:
            if line == tweet_id:
                return 1
            else:
                return -1

def nawab_curate_list(api):
    query = nawab_read_list()
    nawab_search(api, query)
        #time.sleep(60)

def nawab_search(api, query):
    tweet_limit = 1
    
    try:
        last_id = nawab_get_id()
    except FileNotFoundError as e:
        print("No tweet id found")
        last_id = None

    if len(query) > 0:
        for line in query:
            print("starting new query search: \t" + line)
            try:
                for tweets in tweepy.Cursor(api.search, q=line, tweet_mode="extended", 
                        lang='en',).items(tweet_limit):
                    user = tweets.user.screen_name
                    id = tweets.id
                    nawab_store_id(id)
                    url = 'https://twitter.com/' + user +  '/status/' + str(id)
                    print(url)
                print("Id's are stored for this iteration")
            except tweepy.TweepError as e:
                print(e.reason)

def nawab_retweet_tweet(api):
    with open("tid_store.txt", "r") as fp:
        for line in fp:
            tweet_id = int(line)
            print(tweet_id)
            try:
                api.retweet(tweet_id)
            except tweepy.TweepError as e:
                print(e.reason)

def main():
   api = nawab_twitter_authenticate()
   nawab_curate_list(api)
   nawab_retweet_tweet(api)

if __name__ == "__main__":
    main()
