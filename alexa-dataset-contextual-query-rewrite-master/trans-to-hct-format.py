f1 = open('alexa_test.txt', 'r', encoding='utf-8')
f2 = open('alexa_test.tsv', 'w', encoding='utf-8')
f3 = open('alexa_test_pos.tsv', 'w', encoding='utf-8')

from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('/home/lizitong/stanford-corenlp-4.3.2')

def core(s):
    tgs = nlp.pos_tag(s)
    res = ''
    for i in range(len(tgs)):
        if i != 0:
            res = res + ' '
        res = res + tgs[i][1]
    return res

while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    pts = line.split('\t\t')
    prt = ''
    for i in range(len(pts)):
        prt = prt + pts[i]
        if i < len(pts) - 3:
            prt = prt + ' [SEP] '
        elif i == len(pts) - 3:
            prt = prt + ' [CI] '
        elif i == len(pts) - 2:
            prt = prt + '\t'
    print(prt, file=f2)
    prt = ''
    for i in range(len(pts)):
        prt = prt + core(pts[i])
        if i < len(pts) - 3:
            prt = prt + ' [SEP] '
        elif i == len(pts) - 3:
            prt = prt + ' [CI] '
        elif i == len(pts) - 2:
            prt = prt + '\t'
    print(prt, file=f3)