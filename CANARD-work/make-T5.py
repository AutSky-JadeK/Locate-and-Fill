import json

f1 = open('test.txt', 'r', encoding='utf-8')
f2 = open('test-prompt-5571-T5.json-greedy', 'w', encoding='utf-8')
f3 = open('test-prompt-5571-T5-ids-greedy.txt', 'w', encoding='utf-8')
f4 = open('test-prompt-5571-T5-inputs-greedy.txt', 'w', encoding='utf-8')
f5 = open('test-multi-T5-inputs-greedy.txt', 'w', encoding='utf-8')
f6 = open('test-with-mask-greedy.txt', 'w', encoding='utf-8')
f7 = open('greedy-labels.txt', 'w', encoding='utf-8')
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
    multi_s = []
    lbs = []
    for i in range(len(s1)):
        wd = s1[i]
        flag = False
        tmpl = []
        for j in range(pn, len(s2)):
            if s2[j] == wd and len(s1) - i <= len(s2) - j:
                flag = True
                if tmpl != []:
                    #sn.append('[' + cc + ']')
                    cc = chr(ord(cc) + 1)
                    #sn += (['('] + be_replaced + [')'])
                    for ss in sns:
                        ss += be_replaced
                    sns.append(sn + ['<extra_id_0>'] + ['('] + be_replaced + [')'])
                    multi_s = multi_s + ['<extra_id_0>']
                    '''
                    + ['('] + be_replaced + [')']
                    '''
                    
                    
                    
                    tmps.append(tmpl)
                    
                    sn += be_replaced
                    be_replaced = []
                    
                    
                    
                    tmpl = []
                for ss in sns:
                    ss.append(wd)
                sn.append(wd)
                multi_s.append(wd)
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
        sns.append(sn + ['<extra_id_0>'] + ['('] + be_replaced + [')'])
        multi_s = multi_s + ['<extra_id_0>']
        '''
        if sns != [] and cona(sns[-1]) == 'what happen in 1992 [MASK]':
            print(sns)
            print(pn)
            print(len(s2))
        '''
        
        tmps.append(s2[pn:])
        
        sn += be_replaced
    
    lin = ''
    
    
    for sen in pts[:-2]:
        if lin != '':
            lin = lin + ' [SEP] '
        lin = lin + sen
    for j in range(len(sns)):
        prt={'text': lin + ' [SEP] ' + cona(sns[j]),
        'summary': cona(tmps[j])}
        print(json.dumps(prt), file=f2)
        print(id_now, file=f3)
        print(prt['text'], file=f4)
    if len(sns) != 0:
        print(cona(multi_s), file=f5)
    print(line + '\t\t' + (cona(multi_s)).replace('<extra_id_0>', '[MASK]'), file=f6)
    id_now += 1
    
    cnt += 1
    #if cnt == 5571:
    #    break
    