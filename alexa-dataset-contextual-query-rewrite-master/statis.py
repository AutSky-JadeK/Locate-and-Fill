f1 = open('alexa_train.txt', 'r', encoding='utf-8')
f2 = open('alexa_dev.txt', 'r', encoding='utf-8')
f3 = open('alexa_test.txt', 'r', encoding='utf-8')


alllen = 0
allcnt = 0
allrew = 0

def work(fi):
    global alllen
    global allcnt
    global allrew
    while True:
        line = fi.readline()
        line = line.strip()
        if line == '':
            break
        pts = line.split('\t\t')
        if pts[-2] != pts[-1]:
            allrew += 1
        for sen in pts[:-2]:
            alllen += len(sen)
        allcnt += 1

work(f1)
work(f2)
work(f3)

print(alllen/allcnt)
print(allrew/allcnt)