# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 2015

@author: Brian Sandberg

This code generates a map and displays tweets that have been geocoded. The
tweets are read from previously stored Mongo database collections. When the
map is displayed, the user can input different database collections and see
the change in locations relating to the new collection. Scrolling over the 
tweet marker will show the user's screen_name (author). 

This code supports both the JSON format generated from the Twitter API and
a generic format with "x" and "y" for longitude and latitude, respectively.


To execute (@ terminal):

First import file (CSV, JSON, TSV format) into Mongo database:

> mongoimport --db ggs --collection RIposits --type csv --headerline --file c:/gmu/ggs787/project/output/RIposits.csv
> mongoimport --db ggs --collection isis_2014_06 --type tsv --headerline c:/dev/data/S2015_isis/isis_2014-07.tsv
> mongoimport --db ggs --collection syria_2 --type json c:/dev/twitter/output/syria_bb_20150305.json

Second, execute user interface using Processing, Unfolding, and Java:

> java -jar C:/anaconda/Lib/site-packages/processing.py-0202-windows32/processing-py.jar C:/dev/ships_viz_2.py
> java -jar C:/anaconda/Lib/site-packages/processing.py-0202-windows32/processing-py.jar C:/dev/geoviz.py



"""

from de.fhpotsdam.unfolding import UnfoldingMap
from de.fhpotsdam.unfolding.utils import MapUtils
from de.fhpotsdam.unfolding.geo import Location
from de.fhpotsdam.unfolding.data import Feature
from de.fhpotsdam.unfolding.examples.marker.labelmarker import LabeledMarker
from de.fhpotsdam.unfolding.marker import SimplePointMarker
from de.fhpotsdam.unfolding.providers import OpenStreetMap
#from de.fhpotsdam.unfolding.providers import Microsoft

from pymongo import MongoClient
from bson.json_util import dumps

from controlP5 import ControlP5
from controlP5 import Textfield
from controlP5 import ControlListener

#import sentiment
import os

# global variables - declare using global in each function you want to update variables
#font = loadFont("Miso-Light-12.vlw")
font = loadFont("Eureka-24.vlw")

global global_marker_color
global_marker_color = False


def setup():
    
    size(900, 600)
    smooth()

    # Setting up the map
    global map 
    #map = UnfoldingMap(this)
    map = UnfoldingMap(this, OpenStreetMap.OpenStreetMapProvider())
#    map = UnfoldingMap(this, Microsoft.AerialProvider())
    map.zoomToLevel(6)
    map.panTo(Location(34.5, 36.0))
    MapUtils.createDefaultEventDispatcher(this, map)
    global mmanager
    mmanager = map.getDefaultMarkerManager()


    # text field for user input
    global cp5
    cp5 = ControlP5(this)
    cp5.addTextfield("textValue")\
      .setPosition(600, 540)\
      .setSize(140, 30)\
      .setFont(createFont("Times New Roman", 14))\
      .setAutoClear(False)
    textFont(font)
    cp5.getController("textValue").addListener(TextListener())


    # read mongodb
    client = MongoClient()
    global db
    db = client.ggs #Database


    while True:
        try:
            #get list of mongodb collections and input initial collection via terminal
            cols = db.collection_names()
            print "\n\n\nList of MongoDB Collections:\n"
            coll_list = []
            for c in cols:
                print c
                coll_list.append(c)
            print "\n"
            col = raw_input('Input collection: ')
            if col in coll_list:
                break
        except:
            print 
            'Input valid collection name\n'
            
        
    #docs is the collection the user inputs to start with (e.g. db.nats0427)
    global docs
    docs = db[col] #Collection to start with

    global cursor 
    #cursor = docs.find({}) # select all documents
    cursor = docs.find({"coordinates": {"$ne": None}},{"_id":0, "coordinates":1, "user.screen_name":1, "created_at":1}) # select all values with coords
    # Issue: using the "text" field causes error:
    # UnicodeDecodeError: 'utf-8' codec can't decode bytes in position...
 
    print "Number of Tweets with Location", cursor.count()
    drawMarkers(mmanager,cursor)     



def draw():
    #zoom = map.getZoom()
    marker_size = 5
    background(0)  

    markers = mmanager.getMarkers()
    for m in markers:
        if global_marker_color: # use dark blue for markers
            m.setColor(color(25,25,112, 50))
        else: 
            m.setColor(color(255,215,0, 50))
        if not global_marker_color: # use yellow when showing sentiment
            m.setStrokeColor(color(25,25,112));
        else: 
            m.setStrokeColor(color(255,215,0));
        m.setStrokeWeight(marker_size)
    map.draw()


def mouseMoved():
    hitMarker = mmanager.getFirstHitMarker(mouseX, mouseY)
    if hitMarker != None:
        # Select current marker
        hitMarker.setSelected(True)
    else:
        # Deselect all other markers
        markers = mmanager.getMarkers()
        for marker in markers:
           marker.setSelected(False)


def drawMarkers(mmanager, cursor):
    print (cursor.count())
    #delete all markers
    mmanager.clearMarkers()
    # plot tweets by looping through cursor
    screen_name_list = []
    for t in cursor:
        x = t["coordinates"]["coordinates"][0] #longitude
        y = t["coordinates"]["coordinates"][1] #latitude
        #screen_name = t["created_at"]
        screen_name = t["user"]["screen_name"]

        #text = t["text"]
        # Issue: using the "text" field causes error:
        # UnicodeDecodeError: 'utf-8' codec can't decode bytes in position...
        #text = str.decode(t["text"]) #, errors='ignore')
        #text = unicode(t["text"], "ISO-8859-1")
        #m = SimplePointMarker(Location(y,x))

        m = LabeledMarker(Location(y,x), screen_name, font, 3)
        #m = LabeledMarker(Location(x,y),text, font, 10)
        screen_name_list.append(screen_name)
        global_marker_color = False
        mmanager.addMarker(m)
       

def drawMarkers_sentiment(mmanager, cursor):
    print (cursor.count())
    #delete all markers
    mmanager.clearMarkers()
    # plot tweets by looping through cursor
    screen_name_list = []
    for t in cursor:
        if t["coordinates"] != None:
            x = t["coordinates"]["coordinates"][0] #longitude
            y = t["coordinates"]["coordinates"][1] #latitude
            #screen_name = t["created_at"]
            screen_name = t["user"]["screen_name"]

            m = LabeledMarker(Location(y,x), screen_name, font, 3)
            #m = LabeledMarker(Location(x,y),text, font, 10)
            screen_name_list.append(screen_name)
            global_marker_color = True
            mmanager.addMarker(m)


def drawMarkers_twitter(mmanager, cursor):
    print (cursor.count())
    #delete all markers
    mmanager.clearMarkers()
    # plot tweets by looping through cursor
    screen_name_list = []
    for t in cursor:
        x = t["x"] #longitude
        y = t["y"] #latitude
        screen_name = t["author"]
        m = LabeledMarker(Location(y,x), screen_name, font, 10)
        screen_name_list.append(screen_name)
        global_marker_color = False
        mmanager.addMarker(m)



def help_info():
    cols = db.collection_names()
    print "\n\n\nList of MongoDB Collections:\n"
    for c in cols:
        print c
    print '\nEnter "MongoDB collection" or "command" in map text box'
    print 'Commands: sentiment, scatter, clusters, graph, bigtweets, help, exit\n'


# add'l class to handle textbox events
# Using textbox to change Mongo collection and resulting geocoded tweets on map

class TextListener(ControlListener):

    def controlEvent(self, e):
        
        try:
            #print '%s -> %s' % (e.getName(), e.getStringValue())
            text = e.getStringValue()
            #print text

            # special case for the twitter collection (not JSON from Twitter API)
            if text=='twitter':
                docs = db[text] #Collection
                cursor = docs.find({},{"_id":0, "x":1, "y":1, "author":1}) 
                print "Number of Tweets with Location", cursor.count()
                drawMarkers_twitter(mmanager, cursor)
                
            elif text=='sentiment':
                # User inputs filter term
                
                while True:
                    try:
                    
                        args = []
                        term = raw_input('>>>[mongodb collection] [filter_term]: ')
                        args = term.split(' ')
                        os.system("C:/dev/polarity.bat %s %s" %(args[0], args[1]))
                        sdocs = args[0]                        
                        sfilter_term = args[1]
                        break
                    except:
                        cols = db.collection_names()
                        print "\n\n\nList of MongoDB Collections:\n"
                        for c in cols:
                            print c
                        print '\nUse proper input for Sentiment Analysis:'

                docs = db[sdocs] #Collection
                #cursor = docs.find({"coordinates": {"$ne": None}},{"_id":0, "coordinates":1, "user.screen_name":1, "created_at":1}) # select all values with coords
                cursor = docs.find({"text": {"$regex": sfilter_term, "$options": 'i'}},{"_id":0, "coordinates":1, "user.screen_name":1, "created_at":1}) # select all values with coords
                print 'Number of Tweets matching '+sfilter_term+': ', cursor.count()
                drawMarkers_sentiment(mmanager, cursor)


            elif text=='help':
                help_info()
        
            elif text=='bigtweets':
                # User inputs filter term
                print 'matplotlib'
                os.system("C:/dev/bigtweets.bat")

            elif text=='scatter':
                # User inputs filter term
                print 'scatter graph'
                os.system("C:/dev/scatter.bat")
                
            elif text=='graph':
                # User inputs filter term
                print 'graph service in development'                

            elif text=='clusters':
                # User inputs filter term
                print 'graph service in development'                

            elif text=='exit':
                # User inputs filter term
                print 'goodbye.'
                exit(0)
                
            # collection (JSON Twitter API)
            else:
                docs = db[text] #Collection
                cursor = docs.find({"coordinates": {"$ne": None}},{"_id":0, "coordinates":1, "user.screen_name":1, "created_at":1}) # select all values with coords
                print "Number of Tweets with Location", cursor.count()
                drawMarkers(mmanager, cursor)
 
        except:
            help_info()
            

