import json

f1 = open('dev.txt', 'r', encoding='utf-8')
f2 = open('dev-mask.txt', 'w', encoding='utf-8')
cnt = 0


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
    for wd in s1:
        flag = False
        for j in range(pn, len(s2)):
            if s2[j] == wd:
                flag = True
                if tmpl != []:
                    #sn.append('[' + cc + ']')
                    cc = chr(ord(cc) + 1)
                    #sn += (['('] + be_replaced + [')'])
                    sn += (['[MASK]'])
                    be_replaced = []
                    tmpl = []
                sn.append(wd)
                pn = j+1
                break
            tmpl.append(s2[j])
        if flag == False:
            be_replaced.append(wd)
    if pn != len(s2):
        #sn.append('[' + cc + ']')
        cc = chr(ord(cc) + 1)
        #sn += (['('] + be_replaced + [')'])
        sn += (['[MASK]'])
    sn_contact = ''
    for i in range(len(sn)):
        if i != 0:
            sn_contact += ' '
        sn_contact += sn[i]
    lin = ''
    for sen in pts[:-2]:
        if lin != '':
            lin = lin + '\t\t'
        lin = lin + sen
    lin = lin + '\t\t' + sn_contact + '\t\t' + pts[-1]
    print(lin, file=f2)
    '''
    cnt += 1
    if cnt == 10:
        break
    '''