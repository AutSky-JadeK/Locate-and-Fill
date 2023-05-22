import json

f1 = open('predict_results_bert-100.txt', 'r', encoding='utf-8')
f2 = open('predict_results_canard.txt', 'r', encoding='utf-8')

f3 = open('predict_results_prompt-5-this.txt', 'r', encoding='utf-8')

ok_contexts = []

while True:
    line = f3.readline()
    line = line.strip()
    if line == '':
        break
    ok_contexts.append((line.split('\t\t'))[:-2])

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
    #print(c1)
    c2 = Minus(pts_ref, pts_bef2)
    #print(c2)
    c3 = Union(c1, c2)
    #print(c3)
    
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
    pts = line.split('\t\t')
    if pts[0:-2] in ok_contexts:
        li1.append(pts)
    
print(len(li1))
now = 0
while True:
    line = f2.readline()
    line = line.strip()
    if line == '':
        break
    pts = line.split('\t\t')
    if pts[0:-3] == li1[now][0:-2]:
        li2.append(pts)
        now = now + 1
        if now == 30:
            break
            
av1, av2 = 0, 0
ids, f1score = [], []
add_words = []

for i in range(len(li1)):
    f1score.append([calc(li2[i][-3], li2[i][-1], li2[i][-3], li2[i][-2]), calc(li2[i][-3], li1[i][-1], li2[i][-3], li2[i][-2])])
    add_words.append(Minus(li1[i][-2].split(' '), li2[i][-3].split(' ')))
    #print(f1score[i])
    av1 = av1 + f1score[i][0]
    av2 = av2 + f1score[i][1]
    ids.append(i)
    
ids = sorted(ids, key=lambda x: f1score[x][1]-f1score[x][0], reverse=True)
    
av1 = av1 / float(len(li1))
av2 = av2 / float(len(li1))
print('av1', av1)
print('av2', av2)

f3 = open('show-prompt-bert-100-canard.txt', 'w', encoding='utf-8')
for sid in ids:
    print('before_rewriting_f1:', f1score[sid][0], end='\n\n', file=f3)
    print('after_rewriting_f1: ', f1score[sid][1], end='\n\n', file=f3)
    print('context:', file=f3)
    for sen in li1[sid][0:-2]:
        print(sen, file=f3)
    print('', file=f3)
    print('before_to_be_rewrite:', li2[sid][-3], end='\n\n', file=f3)
    print('before_predict:      ', li2[sid][-1], end='\n\n', file=f3)
    print('after_to_be_rewrite: ', li1[sid][-2], end='\n\n', file=f3)
    print('after_predict:       ', li1[sid][-1], end='\n\n', file=f3)
    print('gold:                ', li2[sid][-2], end='\n\n', file=f3)
    print('add_words:           ', add_words[sid], end='\n\n', file=f3)
    print('before_union:        ', uns[sid*2], end='\n\n', file=f3)
    print('after_union:         ', uns[sid*2+1], end='\n\n', file=f3)
    print('\n\n\n', file=f3)