import json

f1 = open('test.txt', 'r', encoding='utf-8')
f2 = open('test-gene-mask-one.txt', 'w', encoding='utf-8')
f3 = open('test-gene-mask-one-ids.txt', 'w', encoding='utf-8')
cnt = 0

id_now = 0

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
    s1 = pts[-2].split(' ')
    s2 = pts[-1].split(' ')
    pn = 0
    sn = []
    be_replaced = []
    cc = 'A'
    tmpl = []
    sns = []
    tmps = []
    for wd in s1:
        flag = False
        tmpl = []
        for j in range(pn, len(s2)):
            if s2[j] == wd:
                flag = True
                if tmpl != []:
                    #sn.append('[' + cc + ']')
                    cc = chr(ord(cc) + 1)
                    #sn += (['('] + be_replaced + [')'])
                    for ss in sns:
                        ss += be_replaced
                    sns.append(sn + (['[MASK]']))
                    
                    for tmp in tmps:
                        tmp += be_replaced
                    tmps.append(sn + tmpl)
                    
                    sn += be_replaced
                    be_replaced = []
                    
                    
                    
                    tmpl = []
                for ss in sns:
                    ss.append(wd)
                for tmp in tmps:
                    tmp.append(wd)
                sn.append(wd)
                pn = j+1
                break
            tmpl.append(s2[j])
        if flag == False:
            be_replaced.append(wd)
    if pn != len(s2):
        #sn.append('[' + cc + ']')
        cc = chr(ord(cc) + 1)
        for ss in sns:
            ss += be_replaced
        sns.append(sn + (['[MASK]']))
        '''
        if sns != [] and cona(sns[-1]) == 'what happen in 1992 [MASK]':
            print(sns)
            print(pn)
            print(len(s2))
        '''
        for tmp in tmps:
            tmp += be_replaced
        tmps.append(sn + tmpl)
        
        sn += be_replaced
    
    lin = ''
    
    
    for sen in pts[:-2]:
        if lin != '':
            lin = lin + '\t\t'
        lin = lin + sen
    for j in range(len(sns)):
        prt = lin + '\t\t' + cona(sns[j])
        print(prt, file=f2)
        print(id_now, file=f3)
    if sns == []:
        print(lin + '\t\t' + pts[-2], file=f2)
        print(id_now, file=f3)
    id_now += 1
    if id_now == 100:
        break
    '''
    cnt += 1
    if cnt == 10:
        break
    '''