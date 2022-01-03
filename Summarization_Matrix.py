
import numpy as np
import networkx as nx
from underthesea import word_tokenize, sent_tokenize
from nltk.cluster.util import cosine_distance
import regex as re

def read_document(file_name):
	file = open(file_name,"r",encoding="utf-8")
	data = file.read()
	#text1 = re.sub('[@$#&^*%()"]', "", data)
	text1 = sent_tokenize(data)
	sentences = []
	for sentence in text1 :
		sentences.append(word_tokenize(sentence))
	sentences.pop()
	print(len(sentences))
	return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
	if stopwords is None:
		stopwords = []
	sent1 = [w.lower() for w in sent1]
	sent2 = [w.lower() for w in sent2]
	all_words = list(set(sent1 + sent2))
	vector1 = [0] * len(all_words)
	vector2 = [0] * len(all_words)
	for w in sent1:
		if w in stopwords:
			continue
		vector1[all_words.index(w)] += 1
	for w in sent2:
		if w in stopwords:
			continue
		vector2[all_words.index(w)] += 1
	return 1 - cosine_distance(vector1, vector2)

def build_matrix(sentences,stop_words):
	matrix = np.zeros(len(sentences),len(sentences))
	for idx1 in range(len(sentences)):
		for idx2 in range(len(sentences)):
			if idx1 == idx2:
				continue
			matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stopwords)
	return matrix

def generate_summary(file_name , top_n=5) :
	file = open("stop_word_3.txt", "r", encoding="utf-8")
	stop_words = file.read()
	stopwords =[]
	for w in stop_words:
			stopwords.append(w)
	summarize_text = []
	sentences =  read_document(file_name)
    sentence_similarity_martix = build_matrix(sentences, stopwords)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    print("Indexes of top ranked_sentence order are ", ranked_sentence)
    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))
    print("Summarize Text: \n", ". ".join(summarize_text))


generate_summary("output.txt", 2)




