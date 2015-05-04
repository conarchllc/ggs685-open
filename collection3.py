# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 17:21:41 2015

@author: Brian Sandberg
"""


import tweepy
import json


def get_status_and_coords(screen_name):

    # twitter streaming API and app credentials
    app_auth = "C:/dev/twitter/auth/app_auth.json"
    
    with open(app_auth) as json_file:
        key = json.load(json_file)
        #print(key)
    
    auth = tweepy.OAuthHandler(key["consumer_key"], key["consumer_secret"])
    auth.set_access_token(key["access_token_key"], key["access_token_secret"])
    api = tweepy.API(auth)
    
    
    # get the last 200 tweets from screen_name
    statuses = api.user_timeline(screen_name=screen_name, count=200)
    print 'type of statuses: ', type(statuses)
    
    # prepare coordinates for display in leaflet
    coords=[]
    tweets=[]
    for status in statuses:
        user = status.author
        tweets.append(status.text)        
        #print status.text
        try:
            # flip the lon an lat for display in leaflet
            lon = status.coordinates['coordinates'][0]
            lat = status.coordinates['coordinates'][1]
            coords.append([lat,lon])
        except:
            continue
    #    if user.geo_enabled==True:
    
    print coords
    fn = 'c:/out/users/'+screen_name+'.txt'
    f = open(fn, 'w')
    f.write('text\n'.encode('utf8'))

    for i in range(len(tweets)):
        the_status = tweets[i]
        the_status = the_status.encode('utf8')
#        f.write(the_status.encode('utf8'))
        f.write(the_status)
#        f.write(tweets[i])
        
#        print tweets[i]
        
    f.close()
    
    #print statuses



'''
Test
'''


'''
screen_names:


@YouKuffsHateMe
@Victory4ALLah_
@ssskafisti1
@khadijabx3
@jihadiA32 
@backpackRevived
@Bintmuhammad_ 

@YouKuffsHateMe
@Victory4ALLah_
@ssskafisti1
@khadijabx3
@backpackRevived 

'''


#screen_name = 'atawaakul'
screen_name = 'backpackRevived'
get_status_and_coords(screen_name)

