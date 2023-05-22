f1 = open('test.tsv', 'r', encoding='utf-8')
f2 = open('mudoco_test.txt', 'w', encoding='utf-8')

while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    pts = line.split(' [CI] ')
    res = pts[0].split(' [SEP] ') + pts[1].split('\t')
    prt = ''
    for i in range(len(res)):
        if i != 0:
            prt += '\t\t'
        prt += res[i]
    print(prt, file=f2)