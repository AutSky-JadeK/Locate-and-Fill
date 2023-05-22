f1 = open('test.txt', 'r', encoding='utf-8')
f2 = open('after-bert.txt', 'r', encoding='utf-8')
f3 = open('test-no-gold-bert-100.txt', 'w', encoding='utf-8')

li = []
cnt = 0

while True:
    line = f2.readline()
    line = line.strip()
    if line == '':
        break
    li.append(line)
    
while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    pts = line.split('\t\t')
    pts = pts[0:-1]
    pts[-1] = li[cnt]
    res = ''
    for j in range(len(pts)):
        if j != 0:
            res = res + '\t\t'
        res = res + pts[j]
    print(res, file=f3)
    cnt += 1
    if cnt == 100:
        break