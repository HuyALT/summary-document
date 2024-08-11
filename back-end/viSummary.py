import nltk
import re
from pyvi import ViTokenizer
from gensim.models import KeyedVectors
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

def get_stopwords_list(stop_file_path):
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
    stop_word_list = list(frozenset(stop_set))
    result_list = []
    for stopword in stop_word_list:
        result_list.append(stopword.replace(' ','_'))
    return result_list

def preProcess(contents):
    contents = contents.lower() # chuyển tất cả sang chữ thường
    contents = contents.replace('\n', ' ') # loại bỏ các kí tự ngắt dòng
    contents = contents.strip() # loại bỏ khoảng trắng thừa
    return contents

def division(contents):
    sentences = nltk.sent_tokenize(contents)
    return sentences

def sentenceVector(sentences, stopwords_list):
    sentences_vector_arr = []
    vector_path = 'baomoi.model.bin'
    word2vec = KeyedVectors.load_word2vec_format(vector_path, binary=True) # tải model word2vec
    for sentence in sentences:
        sentence_tokenizer = ViTokenizer.tokenize(sentence) # tách câu thành tập hợp từ
        words = sentence_tokenizer.split(' ')
        num_words = 0
        sentences_vector = np.zeros(400)
        for word in words:
            if word not in stopwords_list and word in word2vec.key_to_index:
                num_words += 1
                sentences_vector += word2vec[word] # tính tổng giá trị vector từ trong câu
        sentences_vector_arr.append(sentences_vector / num_words)  # thêm giá trị đại diện cho câu vào tập hợp
    return sentences_vector_arr

def sentencesCluster(sentences_vec_arr):
    # Lấy tương đương 35% tổng số câu
    n_clusters = len(sentences_vec_arr) * 35 // 100
    kmeans = KMeans(n_clusters)
    kmeans = kmeans.fit(sentences_vec_arr)
    return kmeans

def buildSummary(kmeans, sentences_vec_arr, sentences):
    n_clusters = len(sentences_vec_arr) * 35 // 100
    avg = []
    # Tính giá trị trung bình chỉ số câu của mỗi cụm
    for i in range(n_clusters):
        idx = np.where(kmeans.labels_ == i)[0]
        avg.append(np.mean(idx))
    # Tìm câu gần trung tâm cụm nhất
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, sentences_vec_arr)
    # sắp xếp các cụm dựa trên giá trị trung bình
    ordering = sorted(range(n_clusters), key=lambda k: avg[k])
    # Tạo tóm tắt từ các câu đại diện mỗi cụm
    summary = ' '.join([sentences[closest[idx]] for idx in ordering])
    return summary


def summary(contents):
    stopwords_list = get_stopwords_list('stop_words.txt')
    contents = preProcess(contents)
    sentences = division(contents)

    sentences_vec_arr = sentenceVector(sentences, stopwords_list)
    kmeans = sentencesCluster(sentences_vec_arr)
    summary = buildSummary(kmeans, sentences_vec_arr, sentences)

    return summary