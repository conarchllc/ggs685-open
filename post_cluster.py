# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 07:20:11 2015

@author: Brian Sandberg


Dependencies:

The functions in this file depend on data files in the TSV format produced 
by the parsing fucntion. The parser extracts attributes from the 
Twitter JSON data.


Post similarity measure

Both Levenshtein (edit) distance or taking the difference between two posts 
as the number of words that have to be added or deleted has high time 
complexity

bag-of-word approach (fast and robust)
uses word counts: 
vectorization - for each word in a post, count occurrence and store in vector
  rows = words  columns = posts (value is word occurs in post)
  posts are treated as vectors

calculate Euclidean distance between vectors of all posts and take the nearest
one (too slow)

Use as feature vectors:
- extract salient features from each post and store it as a vector per post
- compute clustering on the vectors
- determine the cluster for the post in question
- from this cluster, fetch a handful of posts that are different from the post
  in question (increases diversity)
 

  
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy as sp
import nltk.stem
import sys
from sklearn.cluster import KMeans
from sklearn import metrics
from collections import Counter
import pandas as pd


def frequent_data(data_path, type_of_list, top_n):
    '''
    type_of_list - string, either 'terms' or 'retweets'
    
    tweets_data_path
    '''
    df = pd.DataFrame()
    
    #read_csv
    tweets_in = df.from_csv(data_path, sep='\t')
    # Create a list of tweets
    tweets_text = tweets_in["text"].tolist()
    tweets_screen_name = tweets_in["screen_name"].tolist()


    stop_words = ['a', 'about', 'above', 'across', 'after', 'afterwards',\
    'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also',\
    'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount',\
    'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway',\
    'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became',\
    'because', 'become', 'becomes', 'becoming', 'been', 'before',\
    'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between',\
    'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot',\
    'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',\
    'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',\
    'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even',\
    'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few',\
    'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for',\
    'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full',\
    'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he',\
    'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon',\
    'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred',\
    'i', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it',\
    'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least', 'less',\
    'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine',\
    'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my',\
    'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next',\
    'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now',\
    'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto',\
    'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',\
    'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're',\
    'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several',\
    'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty',\
    'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes',\
    'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than', 'that',\
    'the', 'their', 'them', 'themselves', 'then', 'thence', 'there',\
    'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these',\
    'they', 'thick', 'thin', 'third', 'this', 'those', 'though', 'three',\
    'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top',\
    'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until',\
    'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what',\
    'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',\
    'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether',\
    'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose',\
    'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your',\
    'yours', 'yourself', 'yourselves']
    
    # added Arabic stop words: in, to, on, before, of
    # added English stop words: rt, mar, 2015
    add_words = ['rt', 'من', 'قبل', 'في']
    
    stop_words = stop_words + add_words

    posts = []
    words = []
    lwords = []
    screen_name = []
    all_words = []
    for post in range(len(tweets_text)):
        # extract all words from each post
        words = tweets_text[post].split()
        for w in words:
            # convert all words to lower case
            #lwords.append(w.decode('utf-8').lower())
            lwords.append(w.lower())
        # remove stop words
        lwords = list(set(lwords) - set(stop_words))
        all_words += lwords
        posts.append(tweets_text[post])
        screen_name.append(tweets_screen_name[post])
        lwords = []
    
#    posts = []
#    words = []
#    all_words = []
#    posts_file = open(tweets_data_path, "r")
#    for post in posts_file:
#        words = post.split()
#        all_words += words
#        posts.append(post)
    
    if type_of_list=='terms':
        
        # output most frequent words
        list_of_words = Counter(all_words).most_common()
        
        for i in range(top_n):
            print list_of_words[i][0], list_of_words[i][1]
            
        return list_of_words

    elif type_of_list=='posts':
        
        # output most ferquent posts
        list_of_posts = Counter(posts).most_common()
        # output most ferquent users
        list_of_users = Counter(screen_name).most_common()

        for i in range(top_n):
            print list_of_posts[i][0], list_of_posts[i][1]
            print '\n'
            
        return list_of_posts
        
    elif type_of_list=='users':
        
        # output most ferquent users
        list_of_users = Counter(screen_name).most_common()

        for i in range(top_n):
            print list_of_users[i][0], list_of_users[i][1]
            #print '\n'
            
        return list_of_users

    else:
        print "error: type_of_list should be 'terms' or 'posts'"



def best_post(new_post):
    
    ''' 
    Count words and represent them as a vector
    '''
    
    english_stemmer = nltk.stem.SnowballStemmer('english')
    
    
    #class StemmedCountVectorizer(CountVectorizer):
    #    def build_analyzer(self):
    #        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
    #        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))
    
    #vectorizer = StemmedCountVectorizer(min_df=1, stop_words='english')
    #decode_error='ignore')
    #print sorted(vectorizer.get_stop_words())
    
    #min_df - words occurring less than value will be dropped (min doc freq)
    #max_df - words occurring more than value will be dropped
    #can be a number or a percentage
    
    class StemmedTfidfVectorizer(TfidfVectorizer):
        def build_analyzer(self):
            analyzer = super(TfidfVectorizer, self).build_analyzer()
            return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))
    
    vectorizer = StemmedTfidfVectorizer(min_df=1, stop_words='english',
                                        decode_error='ignore')
    
    tweets_data_path = 'C:/gmu/ggs685/output/Tweets2_text_en.txt'
    #tweets_data_path = 'C:/gmu/ggs685/output/Tweets_text_only.txt'
    
    posts = []
    words = []
    all_words = []
    posts_file = open(tweets_data_path, "r")
    for post in posts_file:
        words = post.split()
        all_words += words
        posts.append(post)
    
    # output most frequent words
    #print Counter(all_words).most_common()
        
    # output most ferquent posts
    print Counter(posts).most_common()    

    
    X = vectorizer.fit_transform(posts)
    
    num_samples, num_features = X.shape

    print "\n#samples: %d, #features: %d" % (num_samples, num_features)
    #print X
    #print X.toarray().transpose()
    

    
    #feature_names = vectorizer.get_feature_names()
    #print 'Type of feature_name: ', type(feature_names[0])
    #for i in range(len(feature_names)):
    #    #print feature_names[i].encode('utf-8')
    #    print feature_names[i]
    
    
            
    
    # vectorize our new post
    new_post_vec = vectorizer.transform([new_post])
    #print new_post_vec
    #print new_post_vec.toarray()
    
    
    def dist_raw(v1,v2):
        delta = v1-v2
        # norm() calculates Euclidean norm (shortest distance)
        return sp.linalg.norm(delta.toarray())
    
    def dist_norm(v1,v2):
        v1_normalized = v1/sp.linalg.norm(v1.toarray())
        v2_normalized = v2/sp.linalg.norm(v2.toarray())
        delta = v1_normalized - v2_normalized
        # norm() calculates Euclidean norm (shortest distance)
        return sp.linalg.norm(delta.toarray())
    
    best_doc = None
    best_dist = sys.maxint
    best_i = None
    
    for i in range(0, num_samples):
        post = posts[i]
        if post==new_post:
            continue
        post_vec = X.getrow(i)
        d = dist_norm(post_vec, new_post_vec)
        #print '== Post %i with dist=%.2f: %s' % (i,d,post)
        if d < best_dist:
            best_dist = d
            best_i = i
    
    print '\nMost similar post is %i with dist=%.2f' % (best_i, best_dist)
    print '\n',posts[best_i]
    
    
    
    #print set(posts)
    #a = Counter(posts)
    #vals = a.values()
    #vals_s = set(vals)
    #print vals_s
    #print type(a)


def similar_posts(tweets_data_path, new_post, num_clusters, top_n):
    
    
    english_stemmer = nltk.stem.SnowballStemmer('english')
    
    class StemmedTfidfVectorizer(TfidfVectorizer):
        def build_analyzer(self):
            analyzer = super(TfidfVectorizer, self).build_analyzer()
            return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))
    
    vectorizer = StemmedTfidfVectorizer(min_df=1, stop_words='english',
                                        decode_error='ignore')
    
    posts = []
    posts_file = open(tweets_data_path, "r")
    for post in posts_file:
        posts.append(post)
    
    X = vectorizer.fit_transform(posts)
    num_samples, num_features = X.shape
    print "\n#samples: %d, #features: %d" % (num_samples, num_features)
    
    
    #num_clusters = 3  # sp.unique(labels).shape[0]

    km = KMeans(n_clusters=num_clusters, init='k-means++', n_init=1,
                verbose=1)
    
    #clustered = km.fit(X)
    km.fit(X)

    
    # Metrics
    
#    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
#    print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
#    print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
#    print("Adjusted Rand Index: %0.3f" %
#          metrics.adjusted_rand_score(labels, km.labels_))
#    print("Adjusted Mutual Information: %0.3f" %
#          metrics.adjusted_mutual_info_score(labels, km.labels_))
#    print(("Silhouette Coefficient: %0.3f" %
#           metrics.silhouette_score(vectorized, labels, sample_size=1000)))
    
    new_post_vec = vectorizer.transform([new_post])
    new_post_label = km.predict(new_post_vec)[0]
    
    similar_indices = (km.labels_ == new_post_label).nonzero()[0]
    
    similar = []
    for i in similar_indices:
        dist = sp.linalg.norm((new_post_vec - X[i]).toarray())
        similar.append((dist, posts[i]))
    
    similar = sorted(similar)
    print 'Length of similar: ', len(similar)
#    import pdb
#    pdb.set_trace()
    
    show_at_1 = similar[0]
    show_at_2 = similar[len(similar) / 2]
    show_at_3 = similar[-1]
    
#    print(show_at_1)
#    print(show_at_2)
#    print(show_at_3)
    for i in range(top_n):
        print i, similar[i]
        print '\n'



def compare_top_words(files, top_n):
    '''
    function takes in a list of two files and top number of words and computes
    the overlap of top words between the two files
    '''
    #print '*********************  START  **********************'
    words = []
    compare = []
    for i in files:
        #print '^^^^^^^^^^^^^^^^^^  ', i, '^^^^^^^^^^^^^^^^^^'
        results = frequent_data(i, 'terms', top_n)
        for j in range(top_n):
            words.append(results[j][0])
        compare.append(words)
        words=[]
        print '\n'
    
    #print '________________________ Shared Terms ______________________'
    for j in range(top_n):
        if compare[0][j] in compare[1]:
            print compare[0][j]





'''
Test
'''

'''
Set Parameters
'''

syria_cities = 'C:/out/syria_cities_20150303.tsv'

new_post = "ISIS recruiting foreign fighters"
#new_post = "Anonymous is taking down ISIS"

num_clusters = 1

top_n = 20


#Example files:
#isis_ar_20150322.tsv
#isis_ar_20150323.tsv
#isis_ar_20150324.tsv
#isis_ar_20150325a.tsv
#isis_ar_20150325b.tsv
#isis_ar_20150326a.tsv
#isis_ar_20150326b.tsv
#isis_ar_20150327.tsv
#isis_ar_20150328a.tsv
#isis_ar_20150328b.tsv
#isis_ar_20150330.tsv


'''
Methods
'''


'''
filename, ['terms' or 'posts' or 'users'], and number of words/posts/users
'''
#frequent_data('C:/out/isis_ar_20150323.tsv', 'terms', top_n)

#frequent_data('C:/out/isis_ar_20150324.tsv', 'terms', top_n)







ar_posts = ['C:/out/isis_ar_20150328a.tsv', 'C:/out/isis_ar_20150330.tsv']

'''
two filenames and number of words
'''
#compare_top_words(ar_posts, top_n)


isil1 = 'c:/out/isis_en_ar_20150322.tsv'

similar_posts(isil1, new_post, num_clusters, top_n)


#best_post(new_post)












