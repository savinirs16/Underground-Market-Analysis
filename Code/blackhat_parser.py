from bs4 import BeautifulSoup
import urllib
from html.parser import HTMLParser
import shutil
import os
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

def blackHatExtractor(List, DestP):
    for item in List:
        urlLink = item[1]
        rowNumber = item[0]
        print(rowNumber)
        #urlLink = 'https://www.blackhatworld.com/seo/turbo-shot-2-0-high-pr-do-follow-blog-comments-pr6-pr1.428941/'
        DestPath = DestP
        #rowNumber = 140
        if os.path.exists(os.path.join(DestPath, str(rowNumber))):
            shutil.rmtree(os.path.join(DestPath, str(rowNumber)))
            os.mkdir(os.path.join(DestPath, str(rowNumber)))
        else:
            os.mkdir(os.path.join(DestPath, str(rowNumber)))

        with urllib.request.urlopen(urlLink) as response:
           html_doc = response.read()
        soup = BeautifulSoup(html_doc, 'html.parser')   
        mylist = soup.findAll("ol", { "id" : "messageList" })
        if len(mylist) > 0:
            allComment = mylist[0].findAll("li",{"class":"message"})
            if len(allComment) > 0:
                mydivs = allComment[0].find("div",{"class":"messageContent"})
        
                images = mydivs.findAll('img')
        
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
            
                if mydivs is not None:
                    #print(mydivs)
                    with open(os.path.join(DestPath,str(rowNumber),str(rowNumber)+".html"),'w',encoding="utf-8") as f:
                        
                        f.writelines(str(mydivs))      
                    data = strip_tags(str(mydivs))
                    #print(data)
                    with open(os.path.join(DestPath,str(rowNumber),str(rowNumber)+".txt"),'w',encoding="utf-8") as f:
                        f.writelines(data)
        time.sleep(1)