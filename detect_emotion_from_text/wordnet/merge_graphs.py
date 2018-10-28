seeds = ['delightful', 'sad', 'loving', 'angry', 'surprising', 'fearful']

graph_files = [open(x+'_graph.txt') for x in seeds]

vocab = set([])

graph = {}

for f in graph_files:
    lines = f.readlines()
    for line in lines :
        words = line.split()
        vocab.update(words)
        if words[0] in graph:
            continue
        graph[words[0]] = set(words[1:])

f = open('graph.txt', 'w')
for word in graph:
    print >>f, word, ' '.join(graph[word])
f.close()
