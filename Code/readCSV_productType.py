import csv
from sklearn.model_selection import KFold
import numpy as np
import nltk
import string
import RAKE
from string import digits
import cv2
from matplotlib import pyplot as plt

remove_digits = str.maketrans('', '', digits)

Rake = RAKE.Rake(RAKE.SmartStopList())
#translator = str.maketrans('', '', string.punctuation)
numFolds = 10
kf = KFold(n_splits=numFolds)
path = "F:\Semester\Fall2017\Edited.csv"
translator = str.maketrans('', '', string.punctuation)
title = []
content = []
payment = []
paymentImg = []
ind = np.arange(1499)
trainInd = []
testInd = []
with open(path, 'r', encoding="utf8") as csvfile:
    rdr = csv.reader(csvfile, delimiter=',')
    for row in rdr:
        title.append(row[2])
        content.append(row[5])
        pI = row[9]
        if(pI == 'img' or pI == 'video'):
            paymentImg.append('')
        else:
            paymentImg.append(pI)
        if(row[6] == ''):
            payment.append([])
            continue
        pay = row[6].lower()       
        allpay1 = pay.replace(';','/')
        allpay = allpay1.strip()
        allpay = allpay.split('/')
        
        methods = []
        if(len(allpay) != 1):
            for items in allpay:
                items = items.rstrip()
                items = items.lstrip()
                if (items == 'paypal') or (items == 'pp'):
                    methods.append('p')
                elif(items[0] == 'b') or (items[0] == 'B'):
                    methods.append('b')
                elif(items[0] == 'v') or (items[0] == 'V'):
                    methods.append('v')
                elif(items[0] == 'd') or (items[0] == 'D'):
                    methods.append('d')
                elif(items[0] == 'a') or (items[0] == 'A'):
                    methods.append('a')
                elif(items[0] == 'm') or (items[0] == 'M'):
                    methods.append('m')
                else:
                    methods.append('o')
            #print(methods)
            
        payment.append(methods)
        
        
for train, test in kf.split(ind):
    trainInd.append(train)
    testInd.append(test)
   
accu = 0.0
for i in range(10):
    currTrain = trainInd[i]
    currTest = testInd[i]
    trainFeat = []
#    for j in range(len(currTrain)):
#        currTitle = title[currTrain[j]].lower()
#        currTitle = currTitle.translate(None, string.punctuation)
#
#        tokens = nltk.word_tokenize(currTitle)
#        tagged = nltk.pos_tag(tokens)
#        feat = []
#        for t in tagged:
#            #print t[1]
#            if((t[1] == 'NNP') or (t[1] == 'NNPS') or (t[1] == 'NN') or (t[1] == 'NNS')):
#                feat.append(t[0])
#        trainFeat.append(feat)
#        
#    testFeat = []
    predTitle = []
    titles = []
    correctScore = []
    for j in range(len(currTest)):
        predicted = ''
        currContent = content[currTest[j]-1].lower()
        words = nltk.word_tokenize(currContent)
        numWords = 6.7*len(words)
        if(currContent == '-'):
            continue
        currTitle = title[currTest[j]-1].lower()
#        if ('closed' in currTitle) or ('removed' in currTitle) or ('no longer existing' in currTitle):
#            continue        
        if(len(currTitle) !=0):            
            
            newcurrTitle = currTitle.translate(translator)
            nodigit = newcurrTitle.translate(remove_digits)
            tokens = nltk.word_tokenize(nodigit)
            tagged = nltk.pos_tag(tokens)
            #print(nodigit)
            titles.append(nodigit)
            if ('facebook' in nodigit) or ('instagram' in nodigit) or ('twitter' in nodigit) or ('pinterest' in nodigit) or ('snapchat' in nodigit):
                predTitle.append('social media')
            elif ('gmail' in nodigit) or ('yahoo' in nodigit) or ('hotmail' in nodigit) or ('mail' in nodigit):
                predTitle.append('accounts')
            elif('csgo' in nodigit):
                predTitle.append('csgo')
                    
            else:
                output = Rake.run(nodigit, minCharacters = 4, maxWords = 3, minFrequency = 1)
                if len(output) == 0:
                    feat = []
                    for t in tagged:
                        if((t[1] == 'NNP') or (t[1] == 'NNPS') or (t[1] == 'NN') or (t[1] == 'NNS')):
                            feat.append(t[0])
                    predicted = feat[0]
                    
                else:
                    predicted = output[0][0]
                    
            predTitle.append(predicted)
            
            correct = 0.0
            wordsPred = nltk.word_tokenize(predicted)
            for p in predicted:
                if p in currContent:
                    correct += 1
            
        correctScore.append(correct/float(numWords))    
    accu += np.mean(correctScore)
    print(np.mean(correctScore))
print(accu/numFolds)
