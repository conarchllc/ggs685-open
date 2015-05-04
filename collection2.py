# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 07:18:26 2015

@author: Brian Sandberg

Tweepy
API class provides access to the entire twitter RESTful API methods
pagination with Cursor objects

The results of friends and followers assumes the use of a layout engine
for nodes and edges such as Gephi (The Open Graph Viz Platform). Gephi provides
interactive visualization and exploration of ISIS networks on Twitter
(dynamic and hierarchical graphs)

"""

import tweepy
import json


# twitter streaming API and app credentials
app_auth = "C:/dev/twitter/auth/app_auth.json"

with open(app_auth) as json_file:
    key = json.load(json_file)
    #print(key)

auth = tweepy.OAuthHandler(key["consumer_key"], key["consumer_secret"])
auth.set_access_token(key["access_token_key"], key["access_token_secret"])
api = tweepy.API(auth)



def get_timeline():
    '''
    prints out the timeline for the owner of the api
    '''
    my_posts = api.home_timeline()
    for tweet in my_posts:
        print tweet.text


def get_user_info(screen_name):
    '''
    Get the User object for a twitter account screen_name
    Print out name, location, number of friends, and number of followers
    returns tweepy user object
    '''
    user = api.get_user(screen_name)
    print user.screen_name
    print('Name: ' + user.name)
    print('Location: ' + user.location)
    print('Friends: ' + str(user.friends_count))
    print('Followers: ' + str(user.followers_count))
    return user


def get_friends(user):
    '''
    pass in a tweepy user object
    call get_user_info which returns a user object
    '''
    print 'Friends:'
    for friend in user.friends():
        print friend.screen_name

def get_friends2():
    '''
    Iterate through all of the authenticated user's friends
    '''
    for friend in tweepy.Cursor(api.friends).items():
        '''
        Process the friend here
        '''
        #process_friend(friend)
        print friend.screen_name
        
        
def num_friends(screen_name):
    '''
    takes in a screen_name and determines number of friends and followers
    and lists them out
    '''    
    friends = api.friends_ids(screen_name=screen_name)
    print screen_name + ' has ' + str(len(friends)) + ' friends'
    print friends

    followers = api.followers_ids(screen_name)
    print screen_name +' has ' + str(len(followers)) + ' followers'
    print followers


def the_rate_limit():
    rate_limit = api.rate_limit_status()
    print rate_limit


def search(term):
    # 36.216667,37.166667
    
    #my_search = api.search(q=term, lang='en', rpp=10, geocode='36.216667,37.166667, 100mi', show_user=True)
    my_search = api.search(q=term, rpp=100, geocode='36.21,37.16,100mi')
    #search_isis = api.search(q='first', geocode='33,70, 100 mi', show_user=True)
    print my_search


def reverse_geocode(lat, lon):
    '''
    e.g. 36.216667, 37.166667
    Given a lat, lon, looks for places (cities and neighbourhoods) whose IDs
    can be specified in a call to update_status() to appear as the name of the
    location. This call provides a detailed response about the location in
    question; the nearby_places() function should be preferred for getting
    a list of places nearby without great detail.
    
    '''
    print api.reverse_geocode(lat, lon)




    
def get_user_id_str(users):
    '''
    takes in a list of screen_names (users) as strings
    print out user_id_str for each screen_name
    returns 
    '''
    user = []
    user_id_str = []
    for i in range(len(users)):
        user.append(api.get_user(screen_name=users[i]))
        user_id_str.append(str(user[i].id_str))
    print 'user_id_str: ', user_id_str





def get_friends_or_followers(graph_type, users, n=20):
    '''
    takes in a list of screen_names (users) as strings
    
    '''

    for j in range(len(users)):
        print 'User screen_name: ', users[j]

        # Get array of IDs of users following the specified user (followers_ids)
        # Or friends of user (friends_ids)
        
        if graph_type=='followers':

            followers = []
            count=0
            
            for f in tweepy.Cursor(api.followers_ids, screen_name=users[j]).items(n):
        
                temp_user = api.get_user(user_id=f)
                temp_screen_name = temp_user.screen_name
        
                followers.append(str(temp_screen_name))
                #print type(f)
                count+=1
            print followers
            print count
        
            thefile= open('c:/out/followers/seeds/'+users[j]+'.txt','w')
            
            for follower in followers:
                thefile.write(follower + ',' + users[j] + '\n')
                #G.add_edge(users[j],follower)
        
            thefile.close() # you can omit in most cases as the destructor will call if

        elif graph_type=='friends':

            friends = []
            count=0
            
            for f in tweepy.Cursor(api.friends_ids, screen_name=users[j]).items(n):
        
                temp_user = api.get_user(user_id=f)
                temp_screen_name = temp_user.screen_name
        
                friends.append(str(temp_screen_name))
                #print type(f)
                count+=1
            print friends
            print count
        
            thefile= open('c:/out/friends/seeds/'+users[j]+'.txt','w')
            
            for friend in friends:
                thefile.write(friend + ',' + users[j] + '\n')
                #G.add_edge(users[j],follower)
        
            thefile.close() # you can omit in most cases as the destructor will call if



'''
Set Parameters
'''

users = ['khadijabx3']
screen_name = 'Victory4ALLah_'

'''
@YouKuffsHateMe
@Victory4ALLah_
@ssskafisti1

rate limited, start here:
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

'''
Test Methods
'''

get_friends_or_followers('friends', users, n=100)

#get_user_id_str(users)

#get_friends2()

#user_obj = get_user_info(screen_name)
#get_friends(user_obj)

#get_timeline()

#num_friends(screen_name)

#the_rate_limit()

#search('ISIS')

#reverse_geocode(lat=36.216667, lon=37.166667)

