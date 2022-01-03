import numpy as np
from underthesea import word_tokenize,sent_tokenize
from gensim.models import Word2Vec
import bs4 as bs
import urllib.request


content = ''
sentences=[]

def document_input(link):
    global content
    scraped_data = urllib.request.urlopen(link)
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    for tag in parsed_article.find_all(['p','a','strong'], {"class": ["Image","author_mail","description"]}):
        tag.decompose()
    paragraphs = parsed_article.find_all('p')
    for p in paragraphs:
        content += ' ' + p.text
    return content

def PreProcess(text):
    global content
    content = text.lower()
    content = content.replace('\n', '. ')
    content = content.strip()
    return content

def sentences_tokenize(text):
    global sentences
    sents = sent_tokenize(text)
    for sent in sents:
        sentences.append(sent)
    return sentences

def sumary(link,model_path,size):
    global content,sentences
    document_input(link)
    PreProcess(content)
    sentences_tokenize(content)
    model = Word2Vec.load(model_path)
    vocab = model.wv.vocab

    X = []
    for sentence in sentences:
        sentence = word_tokenize(sentence,format="text")
        words = sentence.split(" ")
        sentence_vec = np.zeros((size))
        for word in words:
            if word in vocab:
                sentence_vec += model.wv[word]
        X.append(sentence_vec)

    from sklearn.cluster import KMeans
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans = kmeans.fit(X)

    from sklearn.metrics import pairwise_distances_argmin_min
    avg = []
    for j in range(n_clusters):
        idx = np.where(kmeans.labels_ == j)[0]
        avg.append(np.mean(idx))
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
    ordering = sorted(range(n_clusters), key=lambda k: avg[k])
    summary = ' '.join([sentences[closest[idx]] for idx in ordering])
    print(summary)

sumary('https://vnexpress.net/tp-hcm-xin-duoc-chu-dong-mua-vaccine-covid-19-4294393.html','model/word2vec_3.model',500)
