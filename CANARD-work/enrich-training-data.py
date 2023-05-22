import json
import random

cnt0 = 0

def cona(lis):
    sn_contact = ''
    for i in range(len(lis)):
        if i != 0:
            sn_contact += ' '
        sn_contact += lis[i]
    return sn_contact
    
def cona_sep(lis):
    sn_contact = ''
    for i in range(len(lis)):
        if i != 0:
            sn_contact += ' [SEP] '
        sn_contact += lis[i]
    return sn_contact
    
def check_rep_all_blank(lst1, lst2, p):
    np = p
    edp = 0
    flag = True
    while np < len(lst1):
        if lst2[np] != 'O':
            flag = False
            break
        if np == len(lst1) - 1 or (lst1[np+1] != 'B-REP' and lst1[np+1] != 'I-REP'):
            edp = np
            break
        np += 1
    if flag == True:
        return p, edp
    else:
        return -1, -1

f1 = open('train-becky-prompt-5571-T5.json', 'r', encoding='utf-8')
f2 = open('train-becky-bertcrf.txt', 'r', encoding='utf-8')
f3 = open('predicted_ner_labels_becky-on-training.txt', 'r', encoding='utf-8')
f4 = open('train.txt', 'r', encoding='utf-8')

training_samples = []

while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    training_samples.append(json.loads(line))

while True:
    line = f3.readline()
    line = line.strip()
    if line == '':
        break
    pre_labels = line.split(' ')
    rea_labels = []
    tks = []
    for i in range(len(pre_labels)):
        line = f2.readline()
        line = line.strip()
        pt_2 = line.split('\t')
        tks.append(pt_2[0])
        rea_labels.append(pt_2[1])
    line = f2.readline()
        
    line = f4.readline()
    line = line.strip()
    pts = line.split('\t\t')
    con = pts[:-2]
    
    '''
    if tks == ['what', 'did', 'his', 'parents', 'do', '?', '[EOS]']:
        print(pre_labels)
        print(rea_labels)
        print('')
    '''
    
    for i in range(len(tks)):
        if pre_labels[i] == 'B-REP':
            bg, ed = check_rep_all_blank(pre_labels, rea_labels, i)
            if bg != -1 and ed != -1:
                cur_utt = []
                replaced = []
                for j in range(len(tks)):
                    if j < bg or j > ed:
                        if tks[j] != '[EOS]':
                            cur_utt.append(tks[j])
                    else:
                        if tks[j] != '[EOS]':
                            replaced.append(tks[j])
                        if j == ed:
                            cur_utt.append('<extra_id_0>')
                            cur_utt.append('(')
                            cur_utt = cur_utt + replaced
                            cur_utt.append(')')
                inp = con + [cona(cur_utt)]
                cnt0 += 1
                #print(cona(cur_utt))
                prt = {"text": cona_sep(inp),
                "summary": ""}
                training_samples.append(prt)
        elif pre_labels[i] == 'B-INS' and rea_labels[i] == 'O':
            if (i == 0 or i == len(pre_labels) - 1) and ('else' in tks or 'other' in tks or 'else' in tks):
                continue
            cur_utt = []
            for j in range(len(tks)):
                if j == i:
                    cur_utt.append('<extra_id_0>')
                    cur_utt.append('(')
                    cur_utt.append(')')
                if tks[j] != '[EOS]':
                    cur_utt.append(tks[j])
            inp = con + [cona(cur_utt)]
            #print(cona(cur_utt))
            cnt0 += 1
            prt = {"text": cona_sep(inp),
            "summary": ""}
            training_samples.append(prt)

print('cnt all enrich samples:', cnt0)

f_o = open('train-becky-prompt-5571-T5-enrich.json', 'w', encoding='utf-8')
random.shuffle(training_samples)
for sam in training_samples:
    print(json.dumps(sam), file=f_o)