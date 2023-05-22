f1 = open('alexa_train.txt', 'r', encoding='utf-8')
f2 = open('alexa_dev.txt', 'r', encoding='utf-8')
f3 = open('alexa_test.txt', 'r', encoding='utf-8')
f4 = open('alexa_train_valid_test_wo_context.txt', 'w', encoding='utf-8')

def work(fi):
    li = []
    while True:
        line = fi.readline()
        line = line.strip()
        if line == '':
            break
        pts = line.split('\t\t')
        res = pts[-2] + '\t' + pts[-1]
        li.append(res)
    return li
    
prt = []
prt = prt + work(f1)
prt = prt + work(f2)
prt = prt + work(f3)
for pri in prt:
    print(pri, file=f4)