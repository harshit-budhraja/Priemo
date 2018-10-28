seeds = ['delightful', 'sad', 'loving', 'angry', 'surprising', 'fearful']

graph_files = {x:open(x+'_graph.txt') for x in seeds}

vocab = {x:set([]) for x in seeds}

graphs = {}

for seed in graph_files:
    f = graph_files[seed]
    graphs[seed] = {}
    lines = f.readlines()
    for line in lines :
        words = line.split()
        vocab[seed].update(words)
        if words[0] in graphs[seed]:
            continue
        graphs[seed][words[0]] = set(words[1:])

    
paths = {x:{} for x in seeds}
min_dist = {x:{} for x in seeds}

for seed in graphs :
    paths[seed][seed] = {0:1}
    level = 0
    to_expand = set([seed])
    visited_words = set([])
    while len(to_expand) :
        level += 1
        new_words = set([])
        for word in to_expand :
            if word not in graphs[seed] :
                continue
            children = graphs[seed][word]
            for child in children :
                if child not in min_dist[seed] :
                    min_dist[seed][child] = level
                if child not in paths[seed]:
                    paths[seed][child] = {level:paths[seed][word][level-1]}
                    new_words.add(child)
                elif level not in paths[seed][child] :
                    paths[seed][child][level] = paths[seed][word][level-1]
                else :
                    paths[seed][child][level] += paths[seed][word][level-1]
        to_expand = new_words


weight = {}
level = 0
power = 10
while level < 6 :
    weight[level] = power
    power /= 10.0
    level += 1

weight[5] = 0.0
# weight[4] = 0.0
# weight[3] = 0.0

def metric(word) :
    score = {}
    for seed in paths :
        score[seed] = 0
        if word in paths[seed] :
            for level in paths[seed][word] :
                score[seed] += paths[seed][word][level]*weight[level]
    return score

print metric('surprised')
    
def metric2(word) :
    score = {}
    for seed in min_dist:
        if word in min_dist[seed]:
            score[seed] = 1.0/(min_dist[seed][word]+1)
    return score
    

f = open('scores.txt', 'w')

all_vocab = set([])
for seed in vocab :
    all_vocab.update(vocab[seed])

for word in all_vocab :
    score = metric(word)
    print >>f, word,
    for seed in score :
        print >> f, seed, score[seed],
    print >>f,''
