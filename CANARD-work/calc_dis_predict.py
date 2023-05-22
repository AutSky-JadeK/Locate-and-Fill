import json

'''
the two artists collaborated on many albums , beginning in 1968 when lennon was still a beatle , with unfinished music no.1 : two virgins
was fly the name of another album aside from unfinished music no.1 : two virgins ?
'''


f1 = open('predict_results_canard.txt', 'r', encoding='utf-8')

sumdis, avedis, cnt = 0, 0, 0
diss = {}
last_len = 0
sumlen, avelen, cntdia = 0, 0, 0

while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    pts = line.split('\t\t')
    pts[-2] = pts[-1]
    pts = pts[:-1]
    if len(pts)-1 < last_len:
        sumlen += last_len
        cntdia += 1
    wds = []
    for sen in pts:
        wds.append(sen.split(' '))
    new_wd = []
    for wd in wds[-1]:
        if wd not in wds[-2]:
            new_wd.append(wd)
    dis_new_wd = []
    for i in range(-3, -len(pts)-1, -1):
        for wd in wds[i]:
            while wd in new_wd:
                new_wd.remove(wd)
                dis_new_wd.append([wd, -i-2])
    for wd in new_wd:
        dis_new_wd.append([wd, 0])
        print(wd, pts)
    for pir in dis_new_wd:
        if pir[1] != 0:
            sumdis += pir[1]
            cnt += 1
        if pir[1] in diss.keys():
            diss[pir[1]] = diss[pir[1]] + 1
        else:
            diss[pir[1]] = 1
    last_len = len(pts)-1
    
sumlen += last_len
cntdia += 1
avelen = sumlen / cntdia
print('avelen', avelen)
            
avedis = sumdis / cnt
print('avedis', avedis)
for ke in diss:
    print(ke, diss[ke])