import json

eps = 0.00000001

f1 = open('scorelist-alexa-prompt.txt', 'r')
f2 = open('scorelist-alexa-ours-rule.txt', 'r')
f3 = open('scorelist-compare.txt', 'w')

dic = {}

while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    pts = line.split(' ')
    score = float(pts[0])
    pid = int(pts[-1])
    dic[pid] = {'prompt': score, 'ours-rule': -1.0}
    
while True:
    line = f2.readline()
    line = line.strip()
    if line == '':
        break
    pts = line.split(' ')
    score = float(pts[0])
    pid = int(pts[-1])
    if pid in dic.keys():
        dic[pid]['ours-rule'] = score
    
    
pids = []
for i in range(5571):
    if i in dic.keys() and dic[i]['prompt'] > -eps and dic[i]['ours-rule'] > -eps:
        pids.append(i)
        
pids = sorted(pids, key=lambda x: dic[x]['prompt']-dic[x]['ours-rule'], reverse=True)


cnt1, cnt2, cnt0 = 0, 0, 0
for x in pids:
    if dic[x]['prompt'] - dic[x]['ours-rule'] > eps:
        cnt1 += 1
    elif dic[x]['prompt'] - dic[x]['ours-rule'] < -eps:
        cnt2 += 1
    else:
        cnt0 += 1
    print('id:', str(x).zfill(5), 'prompt:', dic[x]['prompt'], 'ours-rule:', dic[x]['ours-rule'], file=f3)
    
print(cnt1, cnt2, cnt0)