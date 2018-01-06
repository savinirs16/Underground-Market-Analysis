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
imgaccu = 0.0
allFolds = []
foldSet2 = r"F:\Semester\Fall2017\CS591L\CS591Project-Data\Daksha"
foldSet3 = r"F:\Semester\Fall2017\CS591L\CS591Project-Data\Naman"
foldSet1 = r"F:\Semester\Fall2017\CS591L\CS591Project-Data\Srinivas"
import os
files1 = sorted([int(fname) for fname in (os.listdir(foldSet1))])
files2 = sorted([int(fname) for fname in (os.listdir(foldSet2))])
files3 = sorted([int(fname) for fname in (os.listdir(foldSet3))])

for i in range(len(files1)):
    allFolds.append(os.path.join(foldSet1, str(files1[i])))
for i in range(len(files2)):
    allFolds.append(os.path.join(foldSet2, str(files2[i])))
for i in range(len(files3)):
    allFolds.append(os.path.join(foldSet3, str(files3[i])))
    
sift = cv2.xfeatures2d.SIFT_create()
bf = cv2.BFMatcher()

PP1Temp = cv2.imread(r"F:\Semester\Fall2017\PP1.png")
PP1Temp = cv2.cvtColor(PP1Temp, cv2.COLOR_BGR2GRAY)
(PP1Temp_kp, PP1Temp_dec) = sift.detectAndCompute(PP1Temp,None)



PP2Temp = cv2.imread(r"F:\Semester\Fall2017\PP3.png")
PP2Temp = cv2.cvtColor(PP2Temp, cv2.COLOR_BGR2GRAY)
(PP2Temp_kp, PP2Temp_dec) = sift.detectAndCompute(PP2Temp,None)

#img=cv2.drawKeypoints(PP2Temp,PP2Temp_kp, None)
#cv2.imwrite('sift_keypoints.jpg',img)


BTC1Temp = cv2.imread(r"F:\Semester\Fall2017\BTC1.png")
BTC1Temp = cv2.cvtColor(BTC1Temp, cv2.COLOR_BGR2GRAY)
(BTC1Temp_kp, BTC1Temp_dec) = sift.detectAndCompute(BTC1Temp,None)

BTC2Temp = cv2.imread(r"F:\Semester\Fall2017\BTC2.png")
BTC2Temp = cv2.cvtColor(BTC2Temp, cv2.COLOR_BGR2GRAY)
(BTC2Temp_kp, BTC2Temp_dec) = sift.detectAndCompute(BTC2Temp,None)
#PP1Temp = cv2.imread(r"F:\Semester\Fall2017\PP1.png")
#PP1Temp = cv2.cvtColor(PP1Temp, cv2.COLOR_BGR2GRAY)
#(PP1Temp_kp, PP1Temp_dec) = sift.detectAndCompute(PP1Temp,None)

for i in range(numFolds):
    currTrain = trainInd[i]
    currTest = testInd[i]
    predPayment = []
    count = 0
    total = 0
    for j in range(len(currTest)):
        predpay = []        
        currFolds = allFolds[currTest[j]-1]
        #print(currFolds)
        payImg = paymentImg[currTest[j]-1]
        actualPay = payment[currTest[j]-1]
        if(len(actualPay) == 0):
            continue
        total += 1
        num = os.path.basename(currFolds)
        fname = currFolds + '\\' + num + '.txt'
        if(os.path.isfile(fname)):
            txtfile = open(fname, "r",encoding="utf8") 
            text = txtfile.readlines()
            merged = ''.join(text)
            text = merged.lower()
            if ('btc' in text) or ('bitcoin' in text):
                predpay.append('b')
            if ('paypal' in text) or ('pp' in text):
                predpay.append('p')
            if ('visa' in text):
                predpay.append('v')
            if ('discover' in text):
                predpay.append('d')
            if ('amex' in text):
                predpay.append('a')
            if ('mastercard' in text):
                predpay.append('m')
        #found = []
        if(len(payImg) != 0):
            #f = os.listdir(currFolds)
            for f in os.listdir(currFolds):
                if f.endswith(".jpg") or f.endswith(".JPG") or f.endswith(".png") or f.endswith(".PNG"):
                    img = cv2.imread(os.path.join(currFolds, f))
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    (kp, dec) = sift.detectAndCompute(gray,None)
                    if(dec is None):
                        continue
                    else:
                        matches = bf.knnMatch(PP1Temp_dec,dec, k=2)                    # Apply ratio test
                        good = []
                        for m,n in matches:
                            if m.distance < 0.75*n.distance:
                                good.append([m])
                        if(len(good) > 5):
                            predpay.append('p')
                        else:
                            matches = bf.knnMatch(PP2Temp_dec,dec, k=2)                    # Apply ratio test
                            good = []
                            for m,n in matches:
                                if m.distance < 0.75*n.distance:
                                    good.append([m])
                            if(len(good) > 5):
                                predpay.append('p')   
                                
                        matches = bf.knnMatch(BTC1Temp_dec,dec, k=2)                    # Apply ratio test
                        good = []
                        for m,n in matches:
                            if m.distance < 0.75*n.distance:
                                good.append([m])
                        if(len(good) > 5):
                            predpay.append('b')
                        else:
                            matches = bf.knnMatch(BTC2Temp_dec,dec, k=2)                    # Apply ratio test
                            good = []
                            for m,n in matches:
                                if m.distance < 0.75*n.distance:
                                    good.append([m])
                            if(len(good) > 5):
                                predpay.append('b') 
        
        predPayment.append(predpay)
        #print(actualPay)
        #print(predpay)
        for p in predpay:
            if p in actualPay:
                count += 1
                break
    imgaccu += count/float(total)
    print(count)
    print(total)
    print(count/float(total))
    #print(total)
print (imgaccu/numFolds)