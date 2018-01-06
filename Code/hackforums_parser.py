# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 03:30:34 2017
DriverInstallation: https://sites.google.com/a/chromium.org/chromedriver/getting-started

@author: Anon
"""

import os,shutil
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import urllib
import selenium
from selenium import webdriver
import time
import http
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def hackforumExtractor(List,DestP):
    user = 'drive28'
    pwd  = 'Ridedriver28'
    chromedriver = os.path.join(os.getcwd(),'chromedriver.exe')
    os.environ["PATH"] += chromedriver
    browser = webdriver.Chrome(chromedriver)
    browser.get('https://hackforums.net/member.php?action=login')
    
    username = browser.find_element_by_xpath("//*[@id='content']/div/form/table/tbody/tr[2]/td[2]/input")
    password = browser.find_element_by_xpath("//*[@id='content']/div/form/table/tbody/tr[3]/td[2]/input")
    
    username.send_keys(user)
    password.send_keys(pwd)
    browser.find_element_by_xpath("//*[@id='content']/div/form/div/input").click()

    for item in List:
        urlLink = item[1]
        rowNumber = item[0]
        print(rowNumber)
        #urlLink = 'https://hackforums.net/showthread.php?tid=5587508'
        DestPath = DestP
        #rowNumber = 156
        if os.path.exists(os.path.join(DestPath, str(rowNumber))):
            shutil.rmtree(os.path.join(DestPath, str(rowNumber)))
            os.mkdir(os.path.join(DestPath, str(rowNumber)))        
        else:
            os.mkdir(os.path.join(DestPath, str(rowNumber)))
        browser.get(urlLink)
        html_doc = browser.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')   
        mydivs = soup.findAll("div", { "class" : "post_body scaleimages" })
        if len(mydivs) > 0:
            images = mydivs[0].findAll('img')
        
            try:
                counter = 1
                if len(images) > 0:
                    for i in images:
                        link = i['src']
                        filename=link.split('/')[-1]
                        filename = "".join(x for x in filename if x.isalnum() or x is '.')
                        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                           'Accept-Encoding': 'none',
                           'Accept-Language': 'en-US,en;q=0.8',
                           'Connection': 'keep-alive'}
                        temp = urllib.request.urlopen(urllib.request.Request(link,headers=hdr))
                        data = temp.read()
                        f = open(os.path.join(DestPath,str(rowNumber),str(counter) + '_' + filename), 'wb')
                        f.write(data)
                        f.close()
                        from PIL import Image
                        try:
                            im=Image.open(os.path.join(DestPath,str(rowNumber),str(counter) + '_' + filename))
                        except IOError:
                            os.remove(os.path.join(DestPath,str(rowNumber),str(counter) + '_' + filename))
                        counter += 1
            except ValueError:
                counter += 1
            except urllib.error.URLError:
                counter += 1
            except http.client.HTTPException:
                counter+=1
        
            if mydivs[0] is not None:
                #print(mydivs[0])
                with open(os.path.join(DestPath,str(rowNumber),str(rowNumber)+".html"),'w',encoding="utf-8") as f:
                    
                    f.writelines(str(mydivs[0]))      
                data = strip_tags(str(mydivs[0]))
                #print(data)
                with open(os.path.join(DestPath,str(rowNumber),str(rowNumber)+".txt"),'w',encoding="utf-8") as f:
                    f.writelines(data)
        time.sleep(1)