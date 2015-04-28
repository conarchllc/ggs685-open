# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 22:19:40 2015

@author: Brian Sandberg

Process GDELT Data

"""

import pandas as pd
from collections import Counter
import csv
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def get_news(data_path, hdr_path, gfile): #, type_of_list, top_n):
    '''
    type_of_list - string, either 'terms' or 'posts' ('retweets')
    
    tweets_data_path
    '''
    hdr_in = pd.read_csv(hdr_path)
    hdr_list = hdr_in["Feature"].tolist()
     
#    actor1_values= ['SYRIA','SYRIAN', 'SUNNI', 'KURD','ISLAM','ISLAMIC',\
#                    'ISLAMIC MILITANT','SHIITE', 'MUSLIM', 'SHIA']
    actor1_values= ['MUSLIM', 'ISLAM', 'ISLAMIC', 'ISLAMIC MILITANT', 'ISIS', 'ISLAMIC STATE']
    actor2_values= ['SYRIA','SYRIAN', 'SUNNI', 'KURD','ISLAM','ISLAMIC',\
                    'ISLAMIC MILITANT','SHIITE', 'MUSLIM', 'SHIA']
#    type_codes = ['OPP']
    #read_csv
    news_in = pd.read_csv(data_path, sep='\t', index_col=False, header=None, names=hdr_list)
    actor1 = news_in.loc[news_in['Actor1Name'].isin(actor1_values)]
    actor2 = actor1.loc[news_in['Actor2Name'].isin(actor2_values)]
#    actor3 = actor2.loc[news_in['Actor1Type1Code'].isin(type_codes)]
#    print set(actor2['EventRootCode'].tolist())


    table1 = pd.pivot_table(actor2, values='NumArticles', index = ['EventRootCode'], columns=['Actor1Name'], aggfunc=np.sum)
    table2 = pd.pivot_table(actor2, values='NumArticles', index = ['Actor1Geo_CountryCode'], columns=['Actor1Name'], aggfunc=np.sum)
#    # ActionGeo_FeatureID, ActionGeo_CountryCode, ActionGeo_ADM1Code, ActionGeo_CountryCode, Actor1Geo_CountryCode
    #table3 = pd.pivot_table(actor1, values='NumArticles', index = ['EventRootCode'], columns=['Actor1Geo_Long', 'Actor1Geo_Lat'])
#    
    table1.plot(kind='barh', stacked=True, title='NumArticles '+gfile[0:8])
    table2.plot(kind='barh', stacked=True, title='NumArticles '+gfile[0:8])
    actor2.plot(kind='scatter', x='ActionGeo_Long', y='ActionGeo_Lat', title='Event Locations '+gfile[0:8], s=actor2['NumArticles']) #, s=['NumArticles']*200)

 
#    outfile = 'C:/out/gdelt/pivot/pivot_actor1_'+gfile+'.csv'
    outfile = 'C:/out/gdelt/pivot/pivot.csv'
    f = open(outfile, 'a')
    f.write(gfile+'\n')
    
    table1.to_csv(outfile, mode='a')
    table2.to_csv(outfile, mode='a')

    f.close()

    
#Actor1Geo_Type
#Actor1Geo_FullName
#Actor1Geo_CountryCode
#Actor1Geo_ADM1Code
#Actor1Geo_Lat
#Actor1Geo_Long
#Actor1Geo_FeatureID
#Actor2Geo_Type
#Actor2Geo_FullName
#Actor2Geo_CountryCode
#Actor2Geo_ADM1Code
#Actor2Geo_Lat
#Actor2Geo_Long
#Actor2Geo_FeatureID
#ActionGeo_Type
#ActionGeo_FullName
#ActionGeo_CountryCode
#ActionGeo_ADM1Code
#ActionGeo_Lat
#ActionGeo_Long
#ActionGeo_FeatureID

#IsRootEvent
#EventCode
#EventBaseCode
#EventRootCode
#QuadClass
#GoldsteinScale
#NumMentions
#NumSources
#NumArticles
#AvgTone

#Actor1Code - many combinations makes it difficult to query
#Actor1Name - useful, see actor terms
#Actor1CountryCode - useful Syria = 'SYR'
#Actor1KnownGroupCode - no apparant code for ISIS (usually not available)
#Actor1EthnicCode - e.g. 'kur' for Kurd
#Actor1Religion1Code - e.g. MOS, CHR --> SHI,  SUN
#Actor1Religion2Code
#Actor1Type1Code - e.g. OPP = Opposition
#Actor1Type2Code
#Actor1Type3Code
#Actor2Code
#Actor2Name
#Actor2CountryCode
#Actor2KnownGroupCode
#Actor2EthnicCode
#Actor2Religion1Code
#Actor2Religion2Code
#Actor2Type1Code
#Actor2Type2Code
#Actor2Type3Code
   
    
    f = open('C:/out/gdelt/actors/actors_'+gfile+'.csv', 'w')
   
    count=0
    for row in actor2.iterrows():
        index, data = row
        count+=1
#        print 'Action performed by %s upon %s %s' % (data['Actor1Name'], 
#                                                     data['Actor2Name'], 
#                                                     data['SOURCEURL'])
        if str(data['Actor1Geo_CountryCode']) in ['SY', 'IZ']:
            if (data['EventRootCode']) >=17:
                print gfile+': '+ str(data['Actor1Geo_CountryCode'])+':  '+str(data['SOURCEURL'])
                #print 'filename: '+gfile+': '+ str(data['GLOBALEVENTID'])+': '+str(data['SOURCEURL'])
                print '\n'
                
#                INS - Insurgents (rebels)
#                OPP - Political opposition: opposition parties
#                REB - Rebels: armed and violent opposition 
#                SEP - Separatist rebels
#                SPY - State intelligence services
#                UAF - Armed forces


        if str(data['Actor1CountryCode']) == 'nan':
            c1 = 'XXX_'
        else:
            c1 = str(data['Actor1CountryCode'])+'_'
        if str(data['Actor1Name']) == 'nan':
            a1 = 'XXX_'
        else:
            a1 = str(data['Actor1Name'])+'_'
        if str(data['Actor1Type1Code']) == 'nan':
            t1 = 'XXX_'
        else:
            t1 = str(data['Actor1Type1Code'])+'_'
        if str(data['EventCode']) == 'nan':
            e1 = 'XXX'
        else:
            e1 = str(data['EventRootCode'])

        if str(data['Actor2CountryCode']) == 'nan':
            
            c2 = 'XXX_'
        else:
            c2 = str(data['Actor2CountryCode'])+'_'
        if str(data['Actor2Name']) == 'nan':
            a2 = 'XXX_'
        else:
            a2 = str(data['Actor2Name'])+'_'
        if str(data['Actor2Type1Code']) == 'nan':
            t2 = 'XXX'
        else:
            t2 = str(data['Actor2Type1Code'])

        #print c1,a1,t1,c2,a2,t2
        f.write(a1+t1+e1+','+a2+t2+'\n')
    f.close()
    print count
 

#   actor1 = news_in["Actor1Name"].tolist()
#    # Create a list of tweets
#    print len(actor1)    
#    d = Counter(actor1)
#    #d.keys()[i]
#    print d['SYRIA']
#    for i in range(len(d)):
#        if d.values()[i]>1000:
#            print d.keys()[i]
            
    
#    print counts
#    for word in actor1:
#        cnt[word] += 1
#    if cnt
#    print cnt

    
#gdelt_files = ['20150304.export.CSV', '20150305.export.CSV', '20150306.export.CSV',\
#'20150307.export.CSV', '20150308.export.CSV', '20150309.export.CSV', '20150310.export.CSV',\
#'20150311.export.CSV', '20150312.export.CSV', '20150313.export.CSV', '20150314.export.CSV',\
#'20150315.export.CSV', '20150316.export.CSV', '20150317.export.CSV']

gdelt_files = ['20150325.export.CSV']

#gdelt_files = ['all.csv']

for g in gdelt_files:
    data_path = 'C:/data/gdelt/export/'+g
    hdr_path = 'C:/data/gdelt/CSV.header.fieldids.csv'
    get_news(data_path, hdr_path, g)

