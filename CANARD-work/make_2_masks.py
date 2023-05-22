import json
from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('/home1/zitong/stanford-corenlp-4.3.2')

from genderComputer import GenderComputer
gc = GenderComputer()

f1 = open('test.txt', 'r', encoding='utf-8')
f2 = open('tomask-filled-by-human.txt', 'w', encoding='utf-8')
cnt = 0

heshe = ['he', 'him', 'she', 'her', 'his']

def check(st):
    wds2 = st.split(' ')
    for wd in heshe:
        if wd in wds2:
            return True
    return False

def calc_object(ctx):
    nms = []
    for sen in ctx[:1]:
        ner_res = nlp.ner(sen)
        for pir in ner_res:
            nms.append(pir[0])
    boy = 0
    girl = 0
    for nm in nms:
        if gc.resolveGender(nm, None) == 'male':
            boy += 1
        elif gc.resolveGender(nm, None) == 'female':
            girl += 1
    print(boy, girl)
    if boy > girl:
        return 'him'
    elif girl > boy:
        return 'her'
    else:
        return 'this'

while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    cnt += 1
    if cnt == 100 + 1:
        break
    pts = line.split('\t\t')
    
    pts0 = pts[0].split(' ')
    pts2small = (pts[-2].lower()).split(' ')
    flag = False
    for wd in pts0:
        if wd in pts2small:
            flag = True
            break
    if flag == True:
        print(pts[-2], file=f2)
        continue
    
    cixings = nlp.pos_tag(pts[-2])
    depends = nlp.dependency_parse(pts[-2])
    wds = pts[-2].split(' ')
    
    for i in range(len(depends)-1,-1,-1):
        edge = depends[i]
        if (edge[0] == 'nsubj' or edge[0] == 'obj') and cixings[edge[2]-1][1] != 'PRP' and cixings[edge[2]-1][1] != 'WP' and cixings[edge[2]-1][1] != 'DT':
            wds = wds[:edge[2]] + ['[MASK]',calc_object(pts[:-1])] + wds[edge[2]:]
            break
    if check(pts[-2]) == True:
        wds = pts[-2].split(' ')
        '''
    if pts[-2].find('any other') != -1 or pts[-2].find('else') != -1:
        wds = wds[:-1] + ['other','than', 'this'] + [wds[-1]]
        '''
    res = ''
    for j in range(len(wds)):
        if j != 0:
            res = res + ' '
        res = res + wds[j]
    
    
    print(res, file=f2)