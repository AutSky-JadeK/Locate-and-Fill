import json

f1 = open('predict_results_with-before-only-one-mask-100.txt', 'r', encoding='utf-8')
f2 = open('predict_results_canard.txt', 'r', encoding='utf-8')
f3 = open('test-with-before-gene-mask-one-ids.txt', 'r', encoding='utf-8')

li1 = []
li2 = []

def Union(u1, u2):
    c = u2.copy()
    res = []
    for e in u1:
        if e in c:
            c.remove(e)
            res.append(e)
    return res
    
def Minus(u1, u2):
    c = u2.copy()
    res = []
    for e in u1:
        if e in c:
            c.remove(e)
        else:
            res.append(e)
    return res

uns = []

def calc(bef1, pre, bef2, ref):
    pts_bef1 = bef1.split(' ')
    pts_pre = pre.split(' ')
    pts_bef2 = bef2.split(' ')
    pts_ref = ref.split(' ')
    
    c1 = Minus(pts_pre, pts_bef1)
    c2 = Minus(pts_ref, pts_bef2)
    c3 = Union(c1, c2)
    
    uns.append(c3)
    
    if c1 == [] or c2 == [] or c3 == []:
        return 0.0
    
    p = float(len(c3)) / float(len(c1))
    r = float(len(c3)) / float(len(c2))
    f1 = 2 * p * r / (p + r)
    return f1
    
add_words = []

def calcs(bef1s, pres, bef2, ref):
    pts_bef1 = []
    pts_pre = []
    for bef1 in bef1s:
        pts_bef1.append(bef1.split(' '))
    for pre in pres:
        pts_pre.append(pre.split(' '))
    pts_bef2 = bef2.split(' ')
    pts_ref = ref.split(' ')
    
    c1 = []
    for i in range(len(pts_bef1)):
        c1 = c1 + Minus(pts_pre[i], pts_bef1[i])
    #print(c1)
    #print(pts_bef1)
    #print(pts_pre)
    
    
    add_words.append(c1)
    
    c2 = Minus(pts_ref, pts_bef2)
    c3 = Union(c1, c2)
    
    uns.append(c3)
    
    if c1 == [] or c2 == [] or c3 == []:
        return 0.0
    
    p = float(len(c3)) / float(len(c1))
    r = float(len(c3)) / float(len(c2))
    f1 = 2 * p * r / (p + r)
    return f1

while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    li1.append(line.split('\t\t'))
    
bels = []

while True:
    line = f3.readline()
    line = line.strip()
    if line == '':
        break
    bels.append(int(line))
    
now = 0

cntl2 = 0
while True:
    line = f2.readline()
    line = line.strip()
    if line == '':
        break
    li2.append(line.split('\t\t'))
    cntl2 += 1
    if cntl2 == 100:
        break
            
av1, av2 = 0, 0
ids, f1score = [], []

pn = 0

l1s, l2s = [], []

#print(bels)

for i in range(len(li2)):
    l1 = []
    l2 = []
    while pn<len(bels) and bels[pn] == i:
        l1.append(li1[pn][-2])
        l2.append(li1[pn][-1])
        pn += 1
    l1s.append(l1)
    l2s.append(l2)
    f1score.append([calc(li2[i][-3], li2[i][-1], li2[i][-3], li2[i][-2]), calcs(l1, l2, li2[i][-3], li2[i][-2])])
    #add_words.append(Minus(li1[i][-2].split(' '), li2[i][-3].split(' ')))
    #print(f1score[i])
    av1 = av1 + f1score[i][0]
    av2 = av2 + f1score[i][1]
    ids.append(i)
    
ids = sorted(ids, key=lambda x: f1score[x][1]-f1score[x][0], reverse=True)
    
av1 = av1 / float(len(li2))
av2 = av2 / float(len(li2))
print('av1', av1)
print('av2', av2)

cnt1, cnt2, cnt0, cntn = 0, 0, 0, 0

f3 = open('show-with-before-only-one-canard.txt', 'w', encoding='utf-8')
for sid in ids:
    print('before_rewriting_f1:', f1score[sid][0], end='\n\n', file=f3)
    print('after_rewriting_f1: ', f1score[sid][1], end='\n\n', file=f3)
    if f1score[sid][1] > f1score[sid][0]:
        cnt1 += 1
    elif f1score[sid][1] < f1score[sid][0]:
        cnt2 += 1
    else:
        cnt0 += 1
    if f1score[sid][1] > 0:
        cntn += 1
    print('context:', file=f3)
    for sen in li2[sid][0:-2]:
        print(sen, file=f3)
    print('', file=f3)
    print('before_to_be_rewrite:', li2[sid][-3], end='\n\n', file=f3)
    print('before_predict:      ', li2[sid][-1], end='\n\n', file=f3)
    print('after_to_be_rewrite: ', file=f3)
    for sen in l1s[sid]:
        print(sen, file=f3)
    print('', end='\n\n', file=f3)
    print('after_predict:       ', file=f3)
    for sen in l2s[sid]:
        print(sen, file=f3)
    print('', end='\n\n', file=f3)
    print('gold:                ', li2[sid][-2], end='\n\n', file=f3)
    print('add_words:           ', add_words[sid], end='\n\n', file=f3)
    print('before_union:        ', uns[sid*2], end='\n\n', file=f3)
    print('after_union:         ', uns[sid*2+1], end='\n\n', file=f3)
    print('\n\n\n', file=f3)
    
print(cnt1, cnt2, cnt0, cntn)