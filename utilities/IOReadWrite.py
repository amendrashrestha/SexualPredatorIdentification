__author__ = 'amendrashrestha'

import glob
import re
from pathlib import Path

import nltk


def read_text_file(filepath):
    with open(filepath) as content:
        topic_url = content.readlines()
        return topic_url


def cleanText(post):
    post = post.replace("\n", " ").strip()
    post = post.replace("\r", " ").strip()
    post = post.replace("\t", " ").strip()
    return post


def create_file_with_header(filepath, features):
    my_file = Path(filepath)
    if not my_file.exists():
        with open(filepath, 'a') as outcsv:
            features = ','.join(features)
            features = features.replace("\\b", "").replace("\w", "")
            outcsv.write(features)
            outcsv.write("\n")


def get_function_words(filepath):
    with open(filepath, 'r') as f:
        functions = [x.strip() for x in f.readlines()]

        for i in range(0, len(functions)):
            if len(re.findall('\(', functions[i])) == 1 and len(re.findall('\)', functions[i])) == 0:
                functions[i] = functions[i].replace('(', '\(')
            elif len(re.findall('\(', functions[i])) == 0 and len(re.findall('\)', functions[i])) == 1:
                functions[i] = functions[i].replace(')', '\)')
            if functions[i].endswith('*'):
                functions[i] = functions[i].replace('*', '\\w*')
                functions[i] = '\\b' + functions[i]
            else:
                functions[i] = '\\b' + functions[i] + '\\b'
    return functions


def get_wordlist(filepath):
    with open(filepath, 'r') as f:
        tfidf = [x.strip() for x in f.readlines()]

        for i in range(0, len(tfidf)):
            tfidf[i] = '\\b' + tfidf[i] + '\\b'
    return tfidf


def get_LIWC_files(document_path):
    files = sorted([file for file in glob.glob(document_path + '/*', recursive=True)])
    return files


def count_LIWC(filepath):
    LIWC_words = read_text_file(filepath)
    return LIWC_words


def get_most_freq_word(text):
    stopwords = nltk.corpus.stopwords.words('english')
    text = " ".join(text)

    allWords = nltk.tokenize.word_tokenize(text)
    # allWordDist = nltk.FreqDist(w.lower() for w in allWords)

    allWordExceptStopDist = nltk.FreqDist(w.lower() for w in allWords if w.lower() not in stopwords)
    # mostCommon=sorted(w for w in set(allWordExceptStopDist))
    mostCommon = allWordExceptStopDist.most_common(100)
    print(mostCommon)


def get_avg_word_sentence(text):
    sentences = text.split('.')
    sentences = [sentence.split() for sentence in sentences if len(sentence)]
    averages = [sum(len(word) for word in sentence) / len(sentence) for sentence in sentences]
    return averages


def remove_stopword_from_text(text):
    stopwords = nltk.corpus.stopwords.words('english')
    return ' '.join(filter(lambda x: x.lower() not in stopwords, text.split()))


def get_time_category(hour):

    if 1 <= hour <= 4:
        return 0;
    elif 5 <= hour <= 8:
        return 1;
    elif 9 <= hour <= 12:
        return 2;
    elif 13 <= hour <= 16:
        return 3;
    elif 17 <= hour <= 20:
        return 4;
    elif 21 <= hour <= 24:
        return 5;

