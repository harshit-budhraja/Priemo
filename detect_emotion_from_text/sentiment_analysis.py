#!/usr/bin/python
# This is Python script for conducting sentiment analysis on simple text inputs.

import sys
from nltk.corpus import wordnet as wn
import nltk
import os
import string
import sys
import argparse
import math
import re
from os import listdir
from nltk.stem.porter import *
import subprocess
import json

CURR_PATH = str(subprocess.check_output("pwd", shell=True).strip().decode('ascii') + "/detect_emotion_from_text/")


all_jsons = list()

wordnet_score_file = CURR_PATH + 'wordnet/scores.txt'

stemmer = PorterStemmer()
n_chunks = 10

label_list = ['Love','Joy','Sadness','Anger','Surprise','Fear']
colors1 = ['red', 'blue', 'green', 'yellow', 'pink', 'brown'] # colors for plotting each emotion

senti_words = {}

def relation(a,b) :
    ''' Given two words(strings) returns a number that denotes relation between
    the two words.

    Parameters
    ----------
    a : string
    b : string

    Returns
    -------
    float
        relation (less than 1) between two strings

    Notes
    -----
    First it applies BFS on the nltk wordnet and finds the least distance between
    the two given words. If the distance is x the function returns 1/(x+1), else return 0.

    '''
    a = wn.synsets(a)
    b = wn.synsets(b)
    visited_a = set([])
    visited_b = set([])
    stemmed_a = set([])
    stemmed_b = set([])
    depth = 0
    while True:
        if depth > 2:
            return 0
        new_a = set([])
        depth += 1
        for syn in a:
            if stemmer.stem(syn.lemma_names[0]) in stemmed_b:
                return 1.0/depth
            if syn in visited_a:
                continue
            visited_a.add(syn)
            stemmed_a.add(stemmer.stem(syn.lemma_names[0]))
            hyp = set(syn.hyponyms())
            for lemma in syn.lemma_names:
                None
                hyp |= set(wn.synsets(lemma))
            new_a |= hyp
        a = new_a
        new_b = set([])
        depth += 1
        for syn in b:
            if stemmer.stem(syn.lemma_names[0]) in stemmed_a:
                return 1.0/depth
            if syn in visited_b:
                continue
            visited_b.add(syn)
            stemmed_b.add(stemmer.stem(syn.lemma_names[0]))
            hyp = set(syn.hyponyms())
            for lemma in syn.lemma_names:
                None
                hyp |= set(wn.synsets(lemma))
            new_b |= hyp
        b = new_b



# this method has not been used
def relation1_old(a, b) :
    ''' This method takes two words as arguments and returns their similarity based on
    wup_similarity method of nltk wordnet.

    Parameters
    ----------
    a : string
    b : string

    Returns
    -------
    float
        relation between two strings

    References
    ----------
    .. [1] NLTK WordNet <http://www.nltk.org/howto/wordnet.html>

    '''
    syna = wn.synsets(a, pos=wn.NOUN)
    synb = wn.synsets(b, pos=wn.NOUN)
    mx = 0
    mxa = None
    mxb = None
    for i in syna[:1] :
        for j in synb[:1] :
            temp = wn.wup_similarity(i, j)
            if temp != None and temp > mx :
                mx = temp
                mxa = i
                mxb = j
    return mx

wordnet_scores= {}

def load_wordnet() :
    for line in open(wordnet_score_file).readlines() :
        split_line = line.split()
        wordnet_scores[split_line[0]] = {}
        i = 1
        while i < len(split_line) :
            wordnet_scores[split_line[0]][split_line[i]] = float(split_line[i+1])
            i += 2

load_wordnet()

def get_senti_words() :
    ''' initializes the dictionary senti_words with list of seed words for each emotion.

    Notes
    -----
    if `use_only_emotion_names` is True the only the emotion names will be used as seed words
    else files in the directory `sentiments`(which contain related words for each emotion) will be read to
    initialise the dictionary
    '''
    mapping = {
        'love':'loving',
        'joy':'delightful',
        'sadness':'sad',
        'anger':'angry',
        'surprise':'surprising',
        'fear':'fearful'
    }
    use_only_emotion_names = True
    path = CURR_PATH + 'sentiments/'
    files = listdir(path)
    for f in files :
        fopen = open(path+f)
        if use_only_emotion_names:
            senti_words[mapping[f[:-4]]] = [mapping[f[:-4]]]
        else :
            senti_words[f[:-4]] = [x.lower() for x in fopen.read().split()]
    #print (senti_words)


def get_required_pos(pos_tags) :
    ''' filters the array of pos tagged words to allow only the following pos'

    Parameters
    ----------
    pos_tags : array of tuple(string, string)
        list of words with their pos_tags

    Returns
    -------
    answer : array of tuple(string, string)
        list of words which only have the allowed pos_tags

    '''
    required = ['NN', 'JJ', 'VB']
    answer = []
    for token in pos_tags:
        if token[1] in required :
            answer.append(token)
    return answer

def get_imp_words(f) :
    ''' read the file and pos_tag them and return the list after filtering important pos_tagged words

    Parameters
    ----------
    f : string
        filename that has to be read

    Returns
    -------
    imp_words : array of tuple(string, string)
        array of pos_tagged words which are classified as important by
        the function `get_required_pos`
    '''
    text = f.read()
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    imp_words = get_required_pos(pos_tags)
    return imp_words


def get_all_words(f) :
    text = f.read()
    return nltk.word_tokenize(text)

def get_score_of_imp_words_old(imp_words) :
    ''' Get Score for each emotion for the imp_words array of words

    Parameters
    ----------
    imp_words : array of tuple(string, string)

    Returns
    -------
    dictionary (string : float)
        returns mapping of emotions to their score. Sum of the scores of all emotions is 1.
    '''
    all_scores = {}
    score_sum = {}
    max_count = {}
    imp_words = set(imp_words)
    for word in imp_words :
        score = {}
        mx_for_senti = 0;
        mx_senti = ''
        for sentiment in senti_words :
            #score[sentiment] = relation(sentiment, word[0])[0]
            mx = 0
            for senti_word in senti_words[sentiment] :
                mx = max(mx, relation(senti_word, word[0]))
            score[sentiment] = mx
            if sentiment not in score_sum:
                score_sum[sentiment] = mx
            else :
                score_sum[sentiment] += mx
            if mx_for_senti < mx :
                mx_for_senti = mx
                mx_senti = sentiment
        if mx_senti not in max_count:
            max_count[mx_senti] = 1
        else :
            max_count[mx_senti] += 1
        all_scores[word[0]] = score
    sm = 0
    for senti in max_count :
        if senti == '':
            continue
        sm += score_sum[senti]
    score_sum1 = {}
    sm = float(sm)
    for senti in max_count :
        if senti == '':
            continue
        score_sum1[senti] = score_sum[senti]/sm
    return score_sum1


def argmax(dict) :
    mx = 0
    mx_key = ''
    for key in dict :
        if dict[key] > mx :
            mx = dict[key]
            mx_key = key
    return mx_key

def get_score_of_imp_words(imp_words) :
    ''' Get Score for each emotion for the imp_words array of words

    Parameters
    ----------
    imp_words : array of tuple(string, string)

    Returns
    -------
    dictionary (string : float)
        returns mapping of emotions to their score. Sum of the scores of all emotions is 1.
    '''
    score_sum = {}
    count = {}
    count_words = 0
    for sentiment in senti_words :
        score_sum[sentiment] = 0
        count[sentiment] = 0
    for word in imp_words :
        if word not in wordnet_scores :
            continue
        count_words += 1
        if argmax(wordnet_scores[word]) != '' :
            '''if argmax(wordnet_scores[word]) == 'loving' :
                print (word)'''
            count[argmax(wordnet_scores[word])]+=1
        for sentiment in wordnet_scores[word] :
            score_sum[sentiment] += wordnet_scores[word][sentiment]
    tot_score = 0
    for sentiment in score_sum:
        tot_score += score_sum[sentiment]
        #score_sum[sentiment] = score_sum[sentiment]/count_words
    for sentiment in score_sum:
        try:
            score_sum[sentiment] /= tot_score
        except ZeroDivisionError as e:
            #print(e)
            score_sum[sentiment] /= 0.1
    #print (score_sum)
    all_jsons.append(score_sum)
    return score_sum


def text2emo() :
    ''' Reads the arguments
    Reads the input file and splits it into n_chunks parts
    computes score and plots it using plot_data function
    '''

    get_senti_words()

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--output', default = 'sentiment_analysis_results', help = "name of the results folder")
    parser.add_argument("-n", '--n_chunks', type=int, default = 10, help="Set number of chunks the text should be divided into")

    arguments = parser.parse_args()
    n_chunks = arguments.n_chunks

    if not os.path.exists(arguments.output):
        os.makedirs(arguments.output)

    data = {}
    for senti in senti_words :
        data[senti] = []
    words = get_all_words(arguments.infile)
    set_words = [words[i*len(words)//n_chunks:min(len(words),(i+1)*len(words)//n_chunks)] for i in range(n_chunks)]
    toolbar_width = 40
    #sys.stdout.write("Progress : [%s]" % (" " * toolbar_width))
    #sys.stdout.flush()
    #sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    chunk_index = 0
    current_toolbar_width = 0
    for st in set_words :
        score = get_score_of_imp_words(st)
        #print score
        for senti in senti_words :
            if senti in score:
                data[senti].append(score[senti])
            else :
                data[senti].append(0)
        temp = current_toolbar_width
        current_toolbar_width = (chunk_index*toolbar_width)/n_chunks
        #sys.stdout.write('-'*(current_toolbar_width-temp))
        sys.stdout.flush()
        chunk_index+=1
    #sys.stdout.write('\n')


if __name__ == "__main__":
    text2emo()
    delightful = 0
    loving = 0
    surprising = 0
    fearful = 0
    angry = 0
    sad = 0
    #print(all_jsons)
    for myjson in all_jsons:
        delightful += myjson['delightful']
        loving += myjson['loving']
        surprising += myjson['surprising']
        fearful += myjson['fearful']
        angry += myjson['angry']
        sad += myjson['sad']
    final = {
    "delightful": delightful,
    "loving": loving,
    "surprising": surprising,
    "fearful": fearful,
    "angry": angry,
    "sad": sad
    }
    print(json.dumps(final))
