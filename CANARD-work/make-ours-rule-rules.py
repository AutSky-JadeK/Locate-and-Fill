import json

f1_name = 'test-with-mask-greedy.txt'

f1 = open(f1_name, 'r', encoding='utf-8')
f2 = open('test-greedy-prompt-5571-T5-inputs.txt', 'w', encoding='utf-8')
f3 = open('test-greedy-prompt-5571-T5-ids.txt', 'w', encoding='utf-8')
f4 = open('gready-labels.txt', 'w', encoding='utf-8')

def cona(lis):
    sn_contact = ''
    for i in range(len(lis)):
        if i != 0:
            sn_contact += ' '
        sn_contact += lis[i]
    return sn_contact

def gene_prompt_format(s1, s2):
    if f1_name.find('ours-rule') != -1:
        if 'other' in s2 or 'else' in s2 or 'another' in s2:
            s2 = [','] + s2
    p1, p2 = 0, 0
    s3 = []
    #print(s1, s2)
    s3s = []
    
    s3s.append([])
    
    ii = 0
    
    while p1 < len(s1):
        #print(p1, p2)
        if p2 < len(s2) and s1[p1] == s2[p2]:
            s3.append(s1[p1])
            for ss in s3s:
                ss.append(s1[p1])
            p1 += 1
            p2 += 1
        elif s1[p1] == '[MASK_r]':
            #s3s.append(s3 + ['<extra_id_0>', '('])
            s3s[-1] = s3s[-1] + ['<extra_id_' + str(ii) + '>', '(']
            ii += 1
            while p2 < len(s2) and (p1 == len(s1)-1 or s2[p2] != s1[p1+1]):
                s3.append(s2[p2])
                for ss in s3s:
                    ss.append(s2[p2])
                p2 += 1
            s3s[-1].append(')')
            p1 += 1
        elif s1[p1] == '[MASK_i]':
            #s3s.append(s3 + ['<extra_id_0>', '(', ')'])
            s3s[-1] = s3s[-1] + ['<extra_id_' + str(ii) + '>', '(', ')']
            ii += 1
            p1 += 1
        elif p2 < len(s2) and s1[p1] != s2[p2]:
            s3.append(s1[p1])
            for ss in s3s:
                ss.append(s1[p1])
            p1 += 1
            p2 += 1
    return s3s
           
           
           
def get_labels(s1, s2):
    p1, p2 = 0, 0
    
    
    labels = []
    noto = False
    
    while p1 < len(s1):
        #print(p1, p2)
        if p2 < len(s2) and s1[p1] == s2[p2]:
            p1 += 1
            p2 += 1
            if noto == False:
                labels.append('O')
            else:
                noto = False
        elif s1[p1] == '[MASK_r]':
            brep = True
            while p2 < len(s2) and (p1 == len(s1)-1 or s2[p2] != s1[p1+1]):
                if brep == True:
                    brep = False
                    labels.append('B-REP')
                else:
                    labels.append('I-REP')
                p2 += 1
            p1 += 1
        elif s1[p1] == '[MASK_i]':
            #s3s.append(s3 + ['<extra_id_0>', '(', ')'])
            labels.append('B-INS')
            noto = True
            p1 += 1
        elif p2 < len(s2) and s1[p1] != s2[p2]:
            p1 += 1
           
    return labels

cnt = 0           
while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    print(cnt)
    pts = line.split('\t\t')
    if pts[-1].find('[MASK_r]') != -1 or pts[-1].find('[MASK_i]') != -1:
        gene_s = gene_prompt_format(pts[-1].split(' '), pts[-3].split(' '))
        lbs = get_labels(pts[-1].split(' '), pts[-3].split(' '))
        tks = pts[-3].split(' ')
        print(pts[-3])
        print(pts[-1])
        print(lbs)
        for i in range(len(tks)):
            print(tks[i] + '\t' + lbs[i], file=f4)
        print('', file=f4)
        for ss in gene_s:
            if '<extra_id_0>' not in ss:
                continue
            prt = ''
            for i in range(len(pts[:-3])):
                if i != 0:
                    prt += ' [SEP] '
                prt += pts[i]
            prt += (' [SEP] ' + cona(ss))
            print(prt, file=f2)
            print(cnt, file=f3)
    cnt += 1