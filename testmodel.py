import gensim.models.keyedvectors as word2vec

'''model = word2vec.KeyedVectors.load('model/word2vec_3.model')
print('CUỘC_SỐNG')
lists = []
lists = model.wv.most_similar("cuộc_sống")
for list in lists:
    print(list)
'''
import requests
import bs4 as bs
import urllib.request
def document_input(link):
    scraped_data = urllib.request.urlopen(link)
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    content = ''
    for tag in parsed_article.find_all(['p','a','strong'], {"class": ["Image","author_mail","description"]}):
        tag.decompose()
    paragraphs = parsed_article.find_all('p')
    #print(paragraphs)
    for p in paragraphs:
        content += p.text
    print(content)
document_input('https://vnexpress.net/co-gai-cuop-ngan-hang-de-tra-tien-dau-tu-vao-showbiz-4293175.html')


