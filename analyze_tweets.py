# -*- coding: utf-8 -*-
"""
Created on Sun Feb 01 12:43:25 2015

@author: Brian Sandberg

Process tweets 

After print out the count of all tweets in collection

For each keyword (currenlty hard coded), determine the occurrence of each
Extract URLs from each tweet

Extract URLs per keyword

Compute top 5 languages for all tweets

Compute top countries for all tweets


"""

'''
Set Collection Name and Data Path to Twitter JSON Collection

Also set the keywords that will be added as tags to the DataFrame targeting
posts with these keywords -- Links (URLs) will be extracted from the 
relevant tweets

'''

#tweets_data_path = 'C:/dev/twitter/output/isis_mosul_20150131.json'
#tweets_data_path = 'C:/dev/twitter/output/isis_kobani_20150130.json'
#tweets_data_path = 'C:/dev/twitter/output/syria_20150207.json'
#tweets_data_path = 'C:/dev/twitter/output/syria_20150207.json'

#tweets_data_path = 'C:/dev/twitter/output/isis2_20150220.json'
#tweets_data_path = 'C:/dev/twitter/output/isis1_20150124.json'

collection_name = 'texasattack'

tweets_data_path = 'C:/out/twitter/'+collection_name+'.json'

keywords = ['sharia', 'mohammad', 'murder', 'muslim']




import json
import pandas as pd
import matplotlib.pyplot as plt
import re


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
    
    
    

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    
print len(tweets_data)

# put tweets into a pandas DataFrame 
tweets = pd.DataFrame()

# Add columns to DataFrame (text, lang, country)
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

# Plots
tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Language', fontsize=15)
ax.set_ylabel('Posts' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='blue')

tweets_by_country = tweets['country'].value_counts()
print 'tweets_by_country ', tweets_by_country

if len(tweets_by_country) > 0:
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Countries', fontsize=15)
    ax.set_ylabel('Posts' , fontsize=15)
    ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
    tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')



# Compare popularity of ISIS terms and retrieve entities

# Add tags to DataFrame targeting posts with keywords (caliphate, sharia)
# Extract links from the relevants tweets

#keywords = ['Japanese', 'Peshmerga', 'hostage', 'Mosul', 'Obama', 'killed']
#keywords = ['caliphate', 'Mujahid', 'sharia', 'fighter', 'jihad', 'behead', 'kill']
#keywords = ['Aleppo', 'Damascus', 'Homs', 'Latakia', 'Hama', 'Raqqa']
#keywords = ['ISIS', 'DAESH', 'ISIL', 'Islamic State' 'Ø¯Ø§Ø¹Ø´','Ø§Ù„Ø¥Ø³Ù„Ø§Ù…ÙŠØ© Ø¯ÙˆÙ„Ø©' , 'Ø§Ù„Ø¯ÙˆÙ„Ø© Ø§Ù„Ø¥Ø³Ù„Ø§Ù…ÙŠØ© ÙÙŠ Ø§Ù„Ø¹Ø±Ø§Ù‚ ÙˆØ¨Ù„Ø§Ø¯ Ø§Ù„Ø´Ø§Ù…']
#keywords = ['ISIS', 'DAESH', 'ISIL', 'Islamic State', 'IslamicState']

#keywords = ['@', '#']



# count posts for each keyword target

numlist = []
i=0
for k in keywords:
    tweets[k] = tweets['text'].apply(lambda tweet: word_in_text(k, tweet))
    numlist.append(tweets[k].value_counts()[True])
    print 'keyword: ', k, ' count: ', numlist[i]
    i+=1
    

# Comparison chart

x_pos = list(range(len(keywords)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, numlist, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Posts', fontsize=15)
ax.set_title('Ranking of keywords', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(keywords)
plt.grid()


tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))

tweets_with_link = tweets[tweets['link'] != '']

extracted_links= []
for i in range(len(keywords)):
    extracted_links.append ( list(tweets_with_link[tweets_with_link[keywords[i]] == True]['link']))

#print type(extracted_links)
#print extracted_links
#print '\n'

for l in keywords:
    print l+':'
    print tweets_with_link[tweets_with_link[l] == True]['link']
    

'''
Output HTML links that were extracted from posts

'''

from jinja2 import Template
from collections import Counter

template = Template("""
<table>
    {% for item, count in bye.items() %}
        <tr><td><a href={{item}}>{{item}}</a></td><td>{{count}}</td></tr>
    {% endfor %}
</table>
""")

links_to_html = []
for j in range(len(keywords)):
    links_to_html.append ( template.render(bye=Counter(extracted_links[j])))

html_fn = 'c:/out/twitter/'+collection_name+'.html'

f = open(html_fn, 'w')

for k in range(len(keywords)):
    f.write(keywords[k]+':')
    f.write(links_to_html[k].encode('utf8'))

f.close()

