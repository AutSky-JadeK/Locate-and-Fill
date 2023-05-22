f1 = open('mudoco_test.txt', 'r')
f2 = open('predicted_ner_labels_mudoco_becky.txt', 'r')
f3 = open('mudoco_test-with-mask-becky-ner.txt', 'w')

def cona(lis):
    sn_contact = ''
    for i in range(len(lis)):
        if i != 0:
            sn_contact += ' '
        sn_contact += lis[i]
    return sn_contact

while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    pts = line.split('\t\t')
    tks = pts[-2].split(' ')
    line2 = f2.readline()
    line2 = line2.strip()
    labels = line2.split(' ')
    prts = []
    for i in range(len(labels)):
        if i == len(labels)-1:
            if labels[i] == 'B-INS':
                if prts == [] or prts[-1].find('MASK') == -1:
                    prts.append('[MASK_i]')
            break
        if labels[i] == 'O':
            prts.append(tks[i])
        elif labels[i] == 'B-REP':
            if prts == [] or prts[-1].find('MASK') == -1:
                prts.append('[MASK_r]')
        elif labels[i] == 'B-INS':
            if prts == [] or prts[-1].find('MASK') == -1:
                prts.append('[MASK_i]')
            prts.append(tks[i])
    print(line + '\t\t' + cona(prts), file=f3)