#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sun Feb 01 12:43:25 2015

@author: Brian Sandberg
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import re
import unicodedata


def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False
    


def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''
    

# Twitter Collections
    
#tweets_data_path = 'C:/dev/twitter/output/isis1_20150124.json'
#tweets_data_path = 'C:/dev/twitter/output/aleppo_20150228.json'

tweets_data_path = 'C:/dev/twitter/output/isis_ar_20150330.json'




'''
U+000A LINE FEED (\n)
U+000D CARRIAGE RETURN (\r)
U+001C FILE SEPARATOR
U+001D GROUP SEPARATOR
U+001E RECORD SEPARATOR
U+0085 NEXT LINE
U+2028 LINE SEPARATOR
U+2029 PARAGRAPH SEPARATOR

CRLF: Carriage return + line feed, Unicode characters 000D + 000A
LF: Line feed, Unicode character 000A
NEL: Next line, Unicode character 0085
LS: Line separator, Unicode character 2028
PS: Paragraph separator, Unicode character 2029
'''


tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:

    # Decode str to Unicode
    line = line.decode("utf-8")

    # replace Unicode str:
    line = line.replace(u"\u000A", " ") # line feed \n
    line = line.replace(u"\u000B", " ") # vertical tab
    line = line.replace(u"\u000C", " ") # form feed
    line = line.replace(u"\u000D", " ") # carriage return \r
    line = line.replace(u"\u001C", " ") # file separator
    line = line.replace(u"\u001D", " ") # group separator
    line = line.replace(u"\u001E", " ") # record separator
    line = line.replace(u"\u0085", " ") # next line
    line = line.replace(u"\u2028", " ") # line separator
    line = line.replace(u"\u2029", " ") # paragraph separator

    line = line.replace(u"\u000D\u000A", " ") # CR followed by LF

    # Encode back
    line = line.encode("utf-8")

    # try again as a string
    line = line.replace("\\r\\n", " ") # CR followed by LF
    line = line.replace("\\r", " ") # CR
    line = line.replace("\\n", " ") # CR
    #line = line.replace("\\t", " ") # CR
    

    #print line

    try:
        tweet = json.loads(line)
        if 'lang' in tweet:
            tweets_data.append(tweet)
    except:
        continue

print 'Number of Tweets in Collection: ', len(tweets_data)
#print tweets_data[0]
#print tweets_data[20000]

# put tweets into a pandas DataFrame 
tweets = pd.DataFrame()
tweets_text = pd.DataFrame()
tweets_descr = pd.DataFrame()

# Add columns to DataFrame (text, lang, country)
#tweets['id_str'] = map(lambda tweet: tweet['id_str'], tweets_data)
#tweets_text['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
#tweets_text['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['longitude'] = map(lambda tweet: tweet['coordinates']['coordinates'][0] if tweet['coordinates'] != None else None, tweets_data)
tweets['latitude'] = map(lambda tweet: tweet['coordinates']['coordinates'][1] if tweet['coordinates'] != None else None, tweets_data)
#tweets['timestamp'] = map(lambda tweet: tweet['timestamp_ms'], tweets_data)
tweets['created_at'] = map(lambda tweet: tweet['created_at'], tweets_data)

tweets['user_id_str'] = map(lambda tweet: tweet['user']['id_str'], tweets_data)
#tweets['user_name'] = map(lambda tweet: tweet['user']['name'], tweets_data)
#tweets['user_location'] = map(lambda tweet: tweet['user']['location'], tweets_data)
tweets['screen_name'] = map(lambda tweet: tweet['user']['screen_name'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
#tweets_descr['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
#tweets_descr['description'] = map(lambda tweet: tweet['user']['description'], tweets_data)
tweets['description'] = map(lambda tweet: tweet['user']['description'], tweets_data)
tweets['followers'] = map(lambda tweet: tweet['user']['followers_count'], tweets_data)
tweets['friends'] = map(lambda tweet: tweet['user']['friends_count'], tweets_data)
tweets['lists'] = map(lambda tweet: tweet['user']['listed_count'], tweets_data)
tweets['statuses'] = map(lambda tweet: tweet['user']['statuses_count'], tweets_data)
tweets['url'] = map(lambda tweet: tweet['user']['url'], tweets_data)
tweets['user_created_at'] = map(lambda tweet: tweet['user']['created_at'], tweets_data)
tweets['user_timezone'] = map(lambda tweet: tweet['user']['time_zone'], tweets_data)

tweets['pf_image'] = map(lambda tweet: tweet['user']['profile_image_url_https'], tweets_data)
tweets['bg_image'] = map(lambda tweet: tweet['user']['profile_background_image_url_https'], tweets_data)

tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
tweets['country_code'] = map(lambda tweet: tweet['place']['country_code'] if tweet['place'] != None else None, tweets_data)
tweets['placename'] = map(lambda tweet: tweet['place']['name'] if tweet['place'] != None else None, tweets_data)


#tweets['text'] = tweets['text'].str.replace('\n', ' ')
#tweets['text'] = tweets['text'].str.replace('\t', ' ')
#tweets['user_location'] = tweets['user_location'].str.replace('\n', ' ')
#tweets['user_location'] = tweets['user_location'].str.replace('\t', ' ')
#tweets['description'] = tweets['description'].str.replace('\n', ' ')
#tweets['description'] = tweets['description'].str.replace('\t', ' ')


# Outut Tweets to CSV
tweets.to_csv('c:/out/isis_ar_20150330.tsv', mode='w', sep='\t', encoding='utf-8')
#tweets_text.to_csv('c:/gmu/ggs685/output/tweets_text2.tsv', mode='w', sep='\t', encoding='utf-8')
#tweets_descr.to_csv('c:/gmu/ggs685/output/tweets_descr2.tsv', mode='w', sep='\t', encoding='utf-8')


#tweets['background'] = map(lambda tweet: tweet['user']['profile_background_image_url_https'], tweets_data)

#url = tweets['pf_image'].tolist()
#print url[0]
#url2 = tweets['bg_image'].tolist()
#print url2[0]
#
#country = tweets['country'].tolist()
#print 'Country: ', country[0]
#
#import requests
#f = open('C:/dev/twitter/output/images/'+'pic.jpg','wb')
#f.write(requests.get(url[0]).content)
#f.close()
#f = open('C:/dev/twitter/output/images/'+'pic2.jpg','wb')
#f.write(requests.get(url2[0]).content)
#f.close()
#
#
#import goslate
#
#gs = goslate.Goslate()
#src_lang = gs.detect(country[0])
#
#print gs.translate(country[0], 'en', src_lang)



## Plots
#tweets_by_lang = tweets['lang'].value_counts()
#
#fig, ax = plt.subplots()
#ax.tick_params(axis='x', labelsize=15)
#ax.tick_params(axis='y', labelsize=10)
#ax.set_xlabel('Language', fontsize=15)
#ax.set_ylabel('Posts' , fontsize=15)
#ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
#tweets_by_lang[:5].plot(ax=ax, kind='bar', color='blue')
#
#tweets_by_country = tweets['country'].value_counts()
#
#fig, ax = plt.subplots()
#ax.tick_params(axis='x', labelsize=15)
#ax.tick_params(axis='y', labelsize=10)
#ax.set_xlabel('Countries', fontsize=15)
#ax.set_ylabel('Posts' , fontsize=15)
#ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
#tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
#




#
## Compare popularity of ISIS terms and retrieve entities
#
## Add tags to DataFrame targeting posts with keywords (caliphate, sharia)
## Extract links from the relevants tweets
#
#
#keywords = ['isis', 'isil', 'islamicstate', 'daesh', 'Sunni', 'Shia', 'kill']
#
#
## count posts for each keyword target
#
#numlist = []
#i=0
#for k in keywords:
#    tweets[k] = tweets['text'].apply(lambda tweet: word_in_text(k, tweet))
#    numlist.append(tweets[k].value_counts()[True])
#    print 'keyword: ', k, ' count: ', numlist[i]
#    i+=1
#    
#
## Comparison chart
#
#x_pos = list(range(len(keywords)))
#width = 0.8
#fig, ax = plt.subplots()
#plt.bar(x_pos, numlist, width, alpha=1, color='g')
#
## Setting axis labels and ticks
#ax.set_ylabel('Posts', fontsize=15)
#ax.set_title('Ranking of keywords', fontsize=10, fontweight='bold')
#ax.set_xticks([p + 0.4 * width for p in x_pos])
#ax.set_xticklabels(keywords)
#plt.grid()
#
#
#tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))
#
#tweets_with_link = tweets[tweets['link'] != '']
#
#for l in keywords:
#    print l+':'
#    print tweets_with_link[tweets_with_link[l] == True]['link']
#    
