# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23, 2015

@author: Brian Sandberg

Contains functions to interface with Twitter: 

1. twitter_stream_json to collect tweets using term filter
2. twitter_stream__loc_json to collect tweets using term filter
3. send_tweet to post tweet

Uses two different twitter APIs:

1. Python Twitter Tools (ptt) http://mike.verdone.ca/twitter/
   and https://github.com/sixohsix/twitter/tree/master 
   (twitter)
   
2. TwitterAPI https://github.com/geduldig/TwitterAPI
   (TwitterAPI)

https://dev.twitter.com/docs/twitter-libraries for full list of APIs
   
"""

from TwitterAPI import TwitterAPI
from twitter import Twitter
import json
import time

def twitter_stream_json(fn_app_auth, TRACK_TERM, outfile, 
                        num_tweets=0, xduration=0):
    """ (filename, list of strings, filename, int, int) -> None

    fn_app_auth - file of twitter application credential in json format

    TRACK_TERM - list of terms to filter (keywords to track) from Twitter API
    Note: list of keywords are specified as strings and comma-separated
    
    outfile - filename for outputing tweets in json format

    num_tweets - integer for the number of tweets to collect

    xduration - integer for number of seconds to listen for tweets
    
    >>>twitter_stream_json("c:/dev/twitter/auth/app_auth.json",
                        ['#Transcendence', '#Divergent', '#AHauntedHouse2'],
                        "c:/dev/twitter/output/tweets_output.json",
                        1000, 0)
    
    """
    
    with open(fn_app_auth) as json_file:
        key = json.load(json_file)
        #print(key)
    
    api = TwitterAPI(key["consumer_key"], key["consumer_secret"], 
                     key["access_token_key"], key["access_token_secret"])
    
    counter=0
    
    collect=True
    if num_tweets != 0:
        # Stream Tweets:
#        while collect:
#            try:
        r = api.request('statuses/filter', {'track': TRACK_TERM})
        with open(outfile, 'a') as outfile:
            for item in r:
                json.dump(item, outfile)
        
                counter+=1
                if counter < num_tweets:
                    outfile.write('\n')
                    #print counter
                else:
                    break
#            except: # ChunkedEncodingError:
#                continue


    elif xduration != 0:
        
        stop = time.time()+xduration
        # Stream Tweets:
        r = api.request('statuses/filter', {'track': TRACK_TERM})
        with open(outfile, 'a') as outfile:
            for item in r:
                json.dump(item, outfile)

                if time.time() < stop:
                    outfile.write('\n')
                else:
                    break



def twitter_stream_loc_json(fn_app_auth, outfile,
                            num_tweets=0, xduration=0, bb=''):
    """ (filename, list of strings, filename, int, int) -> None

    fn_app_auth - file of twitter application credential in json format
 
    outfile - filename for outputing tweets in json format

    num_tweets - integer for the number of tweets to collect

    xduration - integer for number of seconds to listen for tweets
    
    bb - bounding box with lon, lat for SW followed by lon, lat for NE
    
    >>>twitter_stream_json("c:/dev/twitter/auth/app_auth.json",
                        ['#Transcendence', '#Divergent', '#AHauntedHouse2'],
                        "c:/dev/twitter/output/tweets_output.json",
                        1000, 0)
    
    """
    
    with open(fn_app_auth) as json_file:
        key = json.load(json_file)
        #print(key)
    
    api = TwitterAPI(key["consumer_key"], key["consumer_secret"], 
                     key["access_token_key"], key["access_token_secret"])
    
    counter=0
    
    if num_tweets != 0:
        # Stream Tweets:

        r = api.request('statuses/filter', {'locations': bb})
        with open(outfile, 'a') as outfile:
            for item in r:
                json.dump(item, outfile)
        
                counter+=1
                if counter < num_tweets:
                    outfile.write('\n')
                    #print counter
                else:
                    break
                
    elif xduration != 0:
        
        stop = time.time()+xduration
        # Stream Tweets:
        r = api.request('statuses/filter', {'locations': bb})
        with open(outfile, 'a') as outfile:
            for item in r:
                json.dump(item, outfile)

                if time.time() < stop:
                    outfile.write('\n')
                else:
                    break



def send_tweet(fn_app_auth, my_tweet):
    """ (filename, string) -> int

    Provide filename for your twitter application credential in json format

    Provide string for your tweet 
    
    This function sends a tweet 

    >>> send_tweet("c:/project/app_auth.json", "my tweet")
        
    """

    with open(fn_app_auth) as json_file:
        key = json.load(json_file)
        #print(key)

    #print key (ensure creditials are properly loaded)
    
    # Authentication using tokens and keys
    t = Twitter(auth=OAuth(key["access_token_key"],key["access_token_secret"],
                           key["consumer_key"],key["consumer_secret"]))
    

    # Get your "home" timeline
    #t.statuses.home_timeline()
    
    # Update your status
    t.statuses.update(status=my_tweet)




'''
Test
'''

'''
Set Parameters
'''


'''
twitter streaming API and app credentials

file format:
{"consumer_key": "XXX",
"consumer_secret": "XXX",
"access_token_key": "XXX",
"access_token_secret": "XXX"}
'''

app_auth = "C:/dev/twitter/auth/app_auth.json"


# Set terms to track (filter): e.g. movies of interest 

'''

ISIS Supporter Terms:
الدولة_الإسلامية (Islamic State)
المناصرون (The Supporters)
أنصار (Supporters)


Non-support ISIS

داعشي (Belongs or thinks like DAESH)
الارهابيه (Terrorist)

'''
track_terms = 'الدولة_الإسلامية', 'المناصرون', 'أنصار', 'داعشي', 'الارهابيه'

# file to store json of all tweets matching terms (filter)
outfile = "C:/dev/twitter/output/isis_ar_20150328.json"

# total number of tweets to collect before shutting off stream
num_tweets = 10000

# duration to collect tweets
xduration = 0  # 10800s (3h); 21600s (6h)

# post status
my_tweet = "good to go"

# Bounding Box e,g, Mosul, Iraq (5000 posts, 2520 with location)
bb = '42.90,36.20, 43.32, 36.45'


'''
Methods
'''


# Status Post
#status = send_tweet(app_auth, my_tweet)


# Location Collection
#twitter_stream_loc_json(app_auth, outfile, num_tweets, xduration, bb)


# Topic Collection 
twitter_stream_json(app_auth, track_terms, outfile, num_tweets, xduration)
