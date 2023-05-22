import json

f1 = open('mudoco_test-with-mask-ours-rule-new.txt', 'r', encoding='utf-8')
f2 = open('mudoco_test-ours-rule-new-5571-T5-inputs.txt', 'w', encoding='utf-8')
f3 = open('mudoco_test-ours-rule-new-5571-T5-ids.txt', 'w', encoding='utf-8')

def cona(lis):
    sn_contact = ''
    for i in range(len(lis)):
        if i != 0:
            sn_contact += ' '
        sn_contact += lis[i]
    return sn_contact

def gene_prompt_format(s1, s2):
    if 'other' in s2 or 'else' in s2 or 'another' in s2:
        s2 = [','] + s2
    p1, p2 = 0, 0
    s3 = []
    #print(s1, s2)
    s3s = []
    while p1 < len(s1):
        #print(p1, p2)
        if p2 < len(s2) and s1[p1] == s2[p2]:
            s3.append(s1[p1])
            for ss in s3s:
                ss.append(s1[p1])
            p1 += 1
            p2 += 1
        elif s1[p1] == '[MASK_r]':
            s3s.append(s3 + ['<extra_id_0>', '('])
            while p2 < len(s2) and (p1 == len(s1)-1 or s2[p2] != s1[p1+1]):
                s3.append(s2[p2])
                for ss in s3s:
                    ss.append(s2[p2])
                p2 += 1
            s3s[-1].append(')')
            p1 += 1
        elif s1[p1] == '[MASK_i]':
            s3s.append(s3 + ['<extra_id_0>', '(', ')'])
            p1 += 1
        elif p2 < len(s2) and s1[p1] != s2[p2]:
            s3.append(s1[p1])
            for ss in s3s:
                ss.append(s1[p1])
            p1 += 1
            p2 += 1
    return s3s
           

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
        for ss in gene_s:
            prt = ''
            for i in range(len(pts[:-3])):
                if i != 0:
                    prt += ' [SEP] '
                prt += pts[i]
            prt += (' [SEP] ' + cona(ss))
            print(prt, file=f2)
            print(cnt, file=f3)
    cnt += 1