import json

f1 = open('alexa_train.txt', 'r', encoding='utf-8')
f2 = open('alexa_train-prompt-5571-T5.json', 'w', encoding='utf-8')
f3 = open('alexa_train-prompt-5571-T5-ids.txt', 'w', encoding='utf-8')
f4 = open('alexa_train-prompt-5571-T5-inputs.txt', 'w', encoding='utf-8')
f5 = open('alexa_train-multi-T5-inputs.txt', 'w', encoding='utf-8')
f6 = open('alexa_train-bertcrf.txt', 'w', encoding='utf-8')
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
    labels = []
    for i in range(len(s1)+1):
        labels.append('O')
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
                    if len(be_replaced) == 0:
                        if labels[len(sn)] == 'O':
                            labels[len(sn)] = 'B-INS'
                    else:
                        for k in range(len(be_replaced)):
                            if k == 0:
                                labels[len(sn)+k] = 'B-REP'
                            else:
                                labels[len(sn)+k] = 'I-REP'
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
        if len(be_replaced) == 0:
            if labels[len(sn)] == 'O':
                labels[len(sn)] = 'B-INS'
            else:
                for k in range(len(be_replaced)):
                    if k == 0:
                        labels[len(sn)+k] = 'B-REP'
                    else:
                        labels[len(sn)+k] = 'I-REP'
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
    #print(line + '\t\t' + (cona(multi_s)).replace('<extra_id_0>', '[MASK]'), file=f6)
    s_becky = s1 + ['[EOS]']
    for j in range(len(s_becky)):
        print(s_becky[j] + '\t' + labels[j], file=f6)
    print('', file=f6)
    id_now += 1
    
    cnt += 1
    #if cnt == 5571:
    #    break
    