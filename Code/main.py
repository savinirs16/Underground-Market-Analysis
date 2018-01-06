# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
from blackhat_parser import blackHatExtractor
from hackforums_parser import hackforumExtractor
def readCSV(Path):
    with open(Path,encoding="utf-8") as f:
        data = f.readlines()
    data = [x.split(',')[4] for x in data ] 
    List_black = []
    List_hack  = []

    for item in range(len(data)):
        url = data[item]
        if 'blackhatworld' in url:
            List_black.append((item,url))
        elif 'hackforums' in url:
            List_hack.append((item,url))
        #print(item)
    return List_black,List_hack
b,h=readCSV(r"C:\Users\Anon\Desktop\CS591Project\CyberSecurity And BigData Project - Srinivas.csv")
DestPath=os.path.join(os.getcwd(),'Srinivas')
if len(b) > 0:
    blackHatExtractor(b,DestPath)
if len(h) > 0:
    hackforumExtractor(h,DestPath)
