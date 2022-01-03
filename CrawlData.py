import bs4 as bs
import urllib.request
'''
list_link=open("List_link.txt","r")
lists=list_link.read().splitlines()
#print(len(lists))
article_text = ""
for list in lists:
    #print(list)
    scraped_data = urllib.request.urlopen(list)
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    for tag in parsed_article.find_all(['p','a'], {"class": ["Image","author_mail","description"]}):
        tag.decompose()
    paragraphs = parsed_article.find_all('p')
    #print(paragraphs)
    for p in paragraphs:
        article_text += p.text
#print(type(article_text))
file_save = open('Data/datatrain_2.txt','w',encoding='utf-8')
file_save.write(article_text)'''
import os
import re
path="E:/NienLuan_NLP/Code/Data/Data"
files=os.listdir(path)
article_text = " "

for file in files:
    filepath=path+'/'+file
    text= open(filepath,"r",encoding='utf-8')
    article=text.read()
    article=re.sub(r'(?:(?:http|https):\/\/)?([-a-zA-Z0-9.]{2,256}\.[a-z]{2,4})\b(?:\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?',"",article)
    article = re.sub(r'<[^>]+>','',article)

    article_text += " " + article
    print(article_text)
file_save = open('E:/NienLuan_NLP/Code/Data/Data_PreProcess.txt','w',encoding='utf-8')
file_save.write(article_text)





