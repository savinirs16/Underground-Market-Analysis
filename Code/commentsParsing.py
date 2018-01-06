# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 18:17:57 2017

@author: Anon
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from matplotlib import pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
file1 = open(r"C:\Users\Anon\Desktop\CS591Project\blackhatworld.csv",encoding='latin-1')
data = file1.readlines()
file1.close()
del data[0]
threadID = [ x.split('\t')[3] for x in data ]
sellers =  [ x.split('\t')[1] for x in data ]
sellers =  [ x for x in sellers if x!='' ]
Comments = {}
analyzer = SentimentIntensityAnalyzer()
List     = []
tempList = []
temp = threadID[0]
for i in range(len(threadID)):
    if threadID[i] == temp:
        tempList.append(data[i])
    else:
        List.append(tempList)
        tempList = []
        tempList.append(data[i])
        temp = threadID[i]
        
sent_score_mean = []
sent_score_max  = []
sent_score_posvsneg = []
identifyIndex = []
newSellers = []
for index in range(len(List)):
    print(index)
    item = List[index]
    vals = []
    for i in range( 2 , len(item)):
        sentence = item[i].split('\t')[9]
        sent_tokenize_list = sent_tokenize(sentence)
        for sen in sent_tokenize_list:
            vs = analyzer.polarity_scores(sen)
            #print(sen, vs['compound'])
            vals.append(vs['compound'])
    if len(vals) == 0:
        continue
    newvals = [ x for x in vals if x <= -0.5 or x >= 0.5]
    vals1 = np.asarray(vals)
    mean_val = np.mean(vals1)
    sent_score_max.append(max(vals))
    sent_score_mean.append(mean_val)
    if len(newvals) == 0:
        sent_score_posvsneg.append(0)
    else:
        sent_score_posvsneg.append(np.mean(newvals))
    identifyIndex.append(index)
    newSellers.append(sellers[index])
    
    
newSellers = np.asarray(newSellers)
sent_score_mean = np.asarray(sent_score_mean)
km = KMeans(n_clusters=3)
km.fit(sent_score_mean.reshape(-1,1))    
highest_center = np.argmax(km.cluster_centers_)
pred = km.predict(sent_score_mean.reshape(-1,1))
trustSeller = np.where( pred == highest_center )
trustingSellers = newSellers[trustSeller]
print('Identified %d sellers by taking mean' % len(trustingSellers))

sent_score_max = np.asarray(sent_score_max)
km = KMeans(n_clusters=3)
km.fit(sent_score_max.reshape(-1,1))    
highest_center = np.argmax(km.cluster_centers_)
pred = km.predict(sent_score_max.reshape(-1,1))
trustSeller = np.where( pred == highest_center )
trustingSellers = newSellers[trustSeller]
print('Identified %d sellers by taking max' % len(trustingSellers))

sent_score_posvsneg = np.asarray(sent_score_posvsneg)
km = KMeans(n_clusters=3)
km.fit(sent_score_posvsneg.reshape(-1,1))    
highest_center = np.argmax(km.cluster_centers_)
pred = km.predict(sent_score_posvsneg.reshape(-1,1))
trustSeller = np.where( pred == highest_center )
trustingSellers = newSellers[trustSeller]
lowest_center = np.argmin(km.cluster_centers_)
nonSellers = newSellers[np.where( pred == lowest_center )]
print('Identified %d sellers by taking mean of pos-neg' % len(trustingSellers))

fig, axes = plt.subplots(nrows=3, ncols=1)
fig.tight_layout()
plt.subplot(3,1,1)
plt.plot(sent_score_mean)
plt.xlabel('Mean scores of post')
plt.ylim((-1,1))
plt.subplot(3,1,2)
plt.plot(sent_score_max)
plt.xlabel('Max score of post')
plt.ylim((-1,1))
plt.subplot(3,1,3)
plt.plot(sent_score_posvsneg)
plt.xlabel('Mean score of post removing neutral comments')
plt.ylim((-1,1))
plt.savefig('abc.eps')
#for key, group in itertools.groupby(data1, lambda x: d):
#    print(key , list(group))
#    break