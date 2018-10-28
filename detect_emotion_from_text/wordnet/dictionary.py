import requests
from bs4 import BeautifulSoup

baseurl = "http://www.thesaurus.com/browse/"
adjectivesurl = "/adjective"

def is_ascii(s):
    return all((ord(c) < 128 and c!= ' ') for c in s)

def get_synonyms(word):
    url = baseurl+word
    page  = requests.get(url).text
    soup = BeautifulSoup(page)
    syns = []

    tagset = []

    for syntag in soup.findAll("div", {"class":"filters"}):
        if syntag.find("strong", {"class":"ttl"}) != None:
            for x in syntag.find("strong",{"class":"ttl"}).string.split(", "):
                if is_ascii(x.encode('utf-8')):
                    syns.append(x.encode('utf-8'))
        for td in  syntag.findAll("span", {"class": "text"}):
            if td != None and is_ascii(td.string.encode('utf-8')):
                syns.append(td.string.encode('utf-8'))
    return syns

seeds = ['delightful','loving', 'sad', 'angry', 'surprising', 'fearful']

files = {x:open(x+'_graph.txt', 'w') for x in seeds}

graph = {}


for seed in seeds:
    visited_words = set([])
    level = 0
    to_expand_words = [seed]
    while level < 5:
        level += 1
        new_words = []
        for word in to_expand_words:
            if word in visited_words:
                continue
            print word, level, seed, len(visited_words) 
            syns = get_synonyms(word)
            print >>files[seed], word, ' '.join(syns)
            graph[word] = syns
            for syn in syns:
                new_words.append(syn)
            visited_words.add(word)
        to_expand_words = new_words

