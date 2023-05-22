import json
import nltk
from nltk.translate.bleu_score import corpus_bleu
from rouge import Rouge

space = 100

f1 = open('mudoco_test-becky-ner-5571-T5-outputs.txt', 'r', encoding='utf-8')
f2 = open('mudoco_test.txt', 'r', encoding='utf-8')
f2_ = open('predict_results_mudoco_baseline.txt', 'r', encoding='utf-8')
f3 = open('mudoco_test-becky-ner-5571-T5-ids.txt', 'r', encoding='utf-8')

li1 = []
li2 = []

def Conj(u1, u2):
    c = u2.copy()
    res = []
    for e in u1:
        if e in c:
            c.remove(e)
            res.append(e)
    return res
    
def Minus(u1, u2):
    c = u2.copy()
    res = []
    for e in u1:
        if e in c:
            c.remove(e)
        else:
            res.append(e)
    return res

uns = []

def score_function(ref_n_gram, pred_n_gram, ref_restore, pred_restore):
    ref_restore = set(ref_restore)
    pred_restore = set(pred_restore)
    ref_n_gram = set([ngram_phrase for ngram_phrase in ref_n_gram if set(ngram_phrase) & ref_restore])
    pred_n_gram = set([ngram_phrase for ngram_phrase in pred_n_gram if set(ngram_phrase) & pred_restore])
    inter_count = len(ref_n_gram & pred_n_gram)
    pred_count = len(pred_n_gram)
    ref_count = len(ref_n_gram)
    return inter_count, pred_count, ref_count
    
def restored_count(references, predictions, currents, my, num):
    inter_count_1, pred_count_1, ref_count_1 = [], [], []
    for ref, cand, cur in zip(references, predictions, currents):
        ref_tokens = ref.split(' ')
        pred_tokens = cand.split(' ')
        cur_tokens = cur.split(' ')
        ref_restore_tokens = [token for token in ref_tokens if token not in cur_tokens]
        pred_restore_tokens = [token for token in pred_tokens if token not in cur_tokens]
        if len(ref_restore_tokens) == 0:
            continue
        ref_ngram_1 = list(nltk.ngrams(ref_tokens, n=num))
        pred_ngram_1 = list(nltk.ngrams(pred_tokens, n=num))
        inter_1, pred_1, ref_1 = score_function(ref_ngram_1, pred_ngram_1, ref_restore_tokens, pred_restore_tokens)
        
        inter_count_1.append(inter_1)
        pred_count_1.append(pred_1)
        ref_count_1.append(ref_1)
    
    return inter_count_1, pred_count_1, ref_count_1

def calc_standard_F(restate_str, predict_str, cur_str, num, my=False):
    i1c, p1c, r1c = restored_count(restate_str, predict_str, cur_str, my, num)
    #print(i1c, p1c, r1c)
    total_i1c, total_p1c, total_r1c = 0, 0, 0
    for x in i1c:
        total_i1c += x
    for x in p1c:
        total_p1c += x
    for x in r1c:
        total_r1c += x
    precision = (total_i1c / total_p1c if total_p1c > 0 else 0)
    recall = (total_i1c / total_r1c if total_r1c > 0 else 0)
    fscore = 2 * precision * recall / (precision + recall) if precision > 0 and recall > 0 else 0
    return fscore
    
def calc_bleu(restate_str, predict_str):
    refs_lists = []
    for s in restate_str:
        refs_lists.append([s.split(' ')])
    pres_lists = []
    for s in predict_str:
        pres_lists.append(s.split(' '))
    bleu1s = corpus_bleu(refs_lists, pres_lists, weights=(1.0, 0.0, 0.0, 0.0))
    bleu2s = corpus_bleu(refs_lists, pres_lists, weights=(0.5, 0.5, 0.0, 0.0))
    bleu3s = corpus_bleu(refs_lists, pres_lists, weights=(0.33, 0.33, 0.33, 0.0))
    bleu4s = corpus_bleu(refs_lists, pres_lists, weights=(0.25, 0.25, 0.25, 0.25))
    return bleu1s, bleu2s, bleu3s, bleu4s
    
def calc_EM(restate_str, predict_str):
    res = 0
    for i in range(len(restate_str)):
        if restate_str[i] == predict_str[i]:
            res += 1
    return res / len(restate_str)

def calc_rouge(restate_str, predict_str):
    rouge = Rouge()
    rouge1s = []
    rouge2s = []
    rougels = []
    for ref, cand in zip(restate_str, predict_str):
        flag = False
        if cand.strip() == '' or cand.strip() == '.':
            cand = 'hello'
            flag = True
        rouge_score = rouge.get_scores(cand, ref)
        rouge_1 = rouge_score[0]['rouge-1']['f']
        rouge_2 = rouge_score[0]['rouge-2']['f']
        rouge_l = rouge_score[0]['rouge-l']['f']
        if flag == True:
            rouge_1 = 0.0
            rouge_2 = 0.0
            rouge_l = 0.0
        rouge1s.append(rouge_1)
        rouge2s.append(rouge_2)
        rougels.append(rouge_l)
    return sum(rouge1s) / len(rouge1s), sum(rouge2s) / len(rouge2s), sum(rougels)/len(rougels)

def calc(bef1, pre, bef2, ref):
    pts_bef1 = bef1.split(' ')
    pts_pre = pre.split(' ')
    pts_bef2 = bef2.split(' ')
    pts_ref = ref.split(' ')
    
    c1 = Minus(pts_pre, pts_bef1)
    c2 = Minus(pts_ref, pts_bef2)
    c3 = Conj(c1, c2)
    
    uns.append(c3)
    
    if c1 == [] or c2 == [] or c3 == []:
        return 0.0
    
    p = float(len(c3)) / float(len(c1))
    r = float(len(c3)) / float(len(c2))
    f1 = 2 * p * r / (p + r)
    return f1
    
add_words = []

def calcs(addinmasks, bef2, ref):
    c1 = []
    #print(addinmasks)
    for newwords in addinmasks:
        c1 = c1 + newwords.split(' ')
    pts_bef2 = bef2.split(' ')
    pts_ref = ref.split(' ')
    
    
    #print(c1)
    #print(pts_bef1)
    #print(pts_pre)
    
    
    add_words.append(c1)
    
    c2 = Minus(pts_ref, pts_bef2)
    c3 = Conj(c1, c2)
    
    uns.append(c3)
    
    if c1 == [] or c2 == [] or c3 == []:
        return 0.0
    
    p = float(len(c3)) / float(len(c1))
    r = float(len(c3)) / float(len(c2))
    f1 = 2 * p * r / (p + r)
    return f1

def clean(s):
    res = ''
    for i in range(len(s)):
        if i+1 < len(s) and s[i] == ' ' and (s[i-1] == "'" and s[i+1] == 's') and (i+2 >= len(s) or s[i+2] == ' ') and (i-2 < 0 or s[i-2] == ' '):
            continue
        if i > 1 and (s[i] == '!' or s[i] == '?' or s[i] == "'" or s[i] == ",") and s[i-1] != ' ':
            res = res + ' '
        res = res + s[i]
    return res

cntl2 = 0
while True:
    line = f1.readline()
    line = line.strip()
    li1.append(clean(line))
    cntl2 += 1
    if cntl2 == 545:
        break
    
bels = []

while True:
    line = f3.readline()
    line = line.strip()
    if line == '':
        break
    bels.append(int(line))
    
f3.close()
now = 0

cntl2 = 0
while True:
    line = f2.readline()
    line = line.strip()
    li2.append((line.split('\t\t')) + [''])
    cntl2 += 1
    if cntl2 == 1988:
        break
        

cntl2 = 0
T5_canards = []
while True:
    line = f2_.readline()
    line = line.strip()
    pts_ = line.split('\t\t')
    T5_canards.append(clean(pts_[-1]))
    cntl2 += 1
    if cntl2 == 1988:
        break
            
f_mask = open('mudoco_test-with-mask-becky-ner.txt', 'r')
cnt_mask = 0
mask_utts = []
while True:
    line = f_mask.readline()
    line = line.strip()
    ts = (line.split('\t\t'))[-1]
    ts = ts.replace('[MASK_r]', '[MASK]')
    ts = ts.replace('[MASK_i]', '[MASK]')
    mask_utts.append(ts)
    cnt_mask += 1
    if cnt_mask == 1988:
        break


av1, av2 = 0, 0
ids, f1score = [], []

pn = 0

l1s, l2s = [], []


f4 = open('mudoco_test-becky-ner-5571-T5-inputs.txt', 'r')
li1_inputs = []
while True:
    line = f4.readline()
    line = line.strip()
    if line == '':
        break
    li1_inputs.append(line)


refs, pres, curs = [], [], []
pre2s = []

allhave = 0
ft = open('scorelist-becky-ner-mudoco-5571.txt', 'w')

cases = []

def calc_length(sens):
    res = 0
    for sen in sens:
        res = res + len(sen)
    return res
    
    
def calc_dis(adds, sens):
    sumv, cntv = 0, 0
    for add in adds:
        for wd in add:
            tmp = 0
            for i in range(len(sens)):
                if wd in sens[-i]:
                    tmp = i
                    break
            sumv += tmp
            cntv += 1
    if cntv == 0:
        return 0
    return sumv / cntv
    
    
def bel_group(val):
    global space
    return int(val / space)

for i in range(len(li2)):

    refs.append(li2[i][-2])
    pres.append(li2[i][-1])
    curs.append(li2[i][-3])
    
    if pn >= len(bels) or bels[pn] != i:
        #f1score.append([calc(li2[i][-3], li2[i][-1], li2[i][-3], li2[i][-2]), 1.0])
        #f1score.append([0.0, 0.0])
        
        if li2[i][-2] == li2[i][-3]:
            f1score.append([calc(li2[i][-3], li2[i][-1], li2[i][-3], li2[i][-2]), 1.0])
        else:
            f1score.append([calc(li2[i][-3], li2[i][-1], li2[i][-3], li2[i][-2]), 0.0])
        
        l1s.append([])
        l2s.append([])
        add_words.append([])
        uns.append([])
        uns.append([])
        ids.append(i)
        av1 = av1 + f1score[i][0]
        av2 = av2 + f1score[i][1]
        allhave += 1
        pre2s.append(li2[i][-3])
        
        cases.append({
        'score': f1score[i][1],
        'context_length': calc_length(li2[i][:-3]),
        'masks': 0,
        'dis': 0
        })
        
        continue
    l1 = []
    l2 = []
    
    t_pre = mask_utts[i]
    
    cnt_masks = 0
    
    while pn<len(bels) and bels[pn] == i:
        cnt_masks += 1
        #print(pn, len(li1))
        t_pre = t_pre.replace('[MASK]', li1[pn], 1)
        l1.append(li1[pn])
        l2.append((li1_inputs[pn].split(' [SEP] '))[-1])
        pn += 1
    
    pre2s.append(t_pre)
    
    l1s.append(l1)
    l2s.append(l2)
    f1score.append([calc(li2[i][-3], li2[i][-1], li2[i][-3], li2[i][-2]), calcs(l1, li2[i][-3], li2[i][-2])])
    #add_words.append(Minus(li1[i][-2].split(' '), li2[i][-3].split(' ')))
    #print(f1score[i])
    av1 = av1 + f1score[i][0]
    av2 = av2 + f1score[i][1]
    print(f1score[i][1], 'id:', i, file=ft)
    ids.append(i)
    allhave += 1
    
    cases.append({
        'score': f1score[i][1],
        'context_length': calc_length(li2[i][:-3]),
        'masks': cnt_masks,
        'dis': calc_dis(l1, li2[i][:-3])
        })
    #print(cases[-1])
    
    '''
grps = {}

for case in cases:
    grp = bel_group(case['context_length'])
    if grp not in grps.keys():
        grps[grp] = {'sumv': case['score'],
        'cntv': 1}
    else:
        grps[grp]['sumv'] += case['score']
        grps[grp]['cntv'] += 1
        
#print(grps)
grp_now = 0
while True:
    if grp_now in grps.keys():
        print(round(grps[grp_now]['sumv'] / grps[grp_now]['cntv'], 3), end = ' ')
    else:
        print(0.0, end = ' ')
    grp_now += 1
    if grp_now > 100:
        break
    
print('')
grp_now = 0    
while True:
    if grp_now in grps.keys():
        print(grps[grp_now]['cntv'], end = ' ')
    else:
        print(0.0, end = ' ')
    grp_now += 1
    if grp_now > 100:
        break
        
print('')
grp_now = 0
while True:
    print(str(grp_now * space)+'~'+str((grp_now+1) * space), end = ' ')
    grp_now += 1
    if grp_now > 100:
        break

    '''



    
f_forhuman = open('predict_results_mudoco_becky-ner.txt', 'w', encoding='utf-8')
for sen in pre2s:
    print(sen, file=f_forhuman)





print('')
print('baseline_standard_F1:', calc_standard_F(refs, pres, curs, 1))
#print(pre2s)
print('my_standard_F1:', calc_standard_F(refs, pre2s, curs, 1))
print('T5_canard_standard_F1:', calc_standard_F(refs, T5_canards, curs, 1))



print('')
print('baseline_standard_F2:', calc_standard_F(refs, pres, curs, 2))
#print(pre2s)
print('my_standard_F2:', calc_standard_F(refs, pre2s, curs, 2))
print('T5_canard_standard_F2:', calc_standard_F(refs, T5_canards, curs, 2))

print('baseline:')
print('bleu1 bleu2 bleu3 bleu4')
print(calc_bleu(refs, pres))
print('my:')
print('bleu1 bleu2 bleu3 bleu4')
print(calc_bleu(refs, pre2s))
print('T5_canard:')
print('bleu1 bleu2 bleu3 bleu4')
print(calc_bleu(refs, T5_canards))

print('baseline:')
print('EM')
print(calc_EM(refs, pres))
print('my:')
print('EM')
print(calc_EM(refs, pre2s))
print('T5_canard:')
print('EM')
print(calc_EM(refs, T5_canards))

print('baseline:')
print('rouge1 rouge2 rougeL')
print('baseline_rouge:',calc_rouge(refs, pres))
print('my:')
print('rouge1 rouge2 rougeL')
print('my_rouge:',calc_rouge(refs, pre2s))
print('T5_canard:')
print('rouge1 rouge2 rougeL')
print('T5_canard_rouge:',calc_rouge(refs, T5_canards))


ids = sorted(ids, key=lambda x: f1score[x][1]-f1score[x][0], reverse=True)
    
av1 = av1 / float(allhave)
av2 = av2 / float(allhave)
print('av1', av1)
print('av2', av2)

cnt1, cnt2, cnt0, cntn = 0, 0, 0, 0


f3 = open('show-mudoco-becky-ner-5571-T5.txt', 'w', encoding='utf-8')
for sid in ids:
    if li2[sid][-2] == li2[sid][-3]:
        continue
    print('before_rewriting_f1:', f1score[sid][0], end='\n\n', file=f3)
    print('after_rewriting_f1: ', f1score[sid][1], end='\n\n', file=f3)
    if f1score[sid][1] > f1score[sid][0]:
        cnt1 += 1
    elif f1score[sid][1] < f1score[sid][0]:
        cnt2 += 1
    else:
        cnt0 += 1
    if f1score[sid][1] > 0:
        cntn += 1
    print('id:', str(sid).zfill(5), end='\n\n', file=f3)
    print('context:', file=f3)
    for sen in li2[sid][0:-2]:
        print(sen, file=f3)
    print('', file=f3)
    print('before_to_be_rewrite:', li2[sid][-3], end='\n\n', file=f3)
    print('before_predict:      ', li2[sid][-1], end='\n\n', file=f3)
    print('after_to_be_rewrite: ', file=f3)
    for sen in l2s[sid]:
        print(sen, file=f3)
    print('', end='\n\n', file=f3)
    
    print('after_predict:       ', file=f3)
    for sen in l1s[sid]:
        print(sen, file=f3)
    print('', end='\n\n', file=f3)
    
    print('gold:                ', li2[sid][-2], end='\n\n', file=f3)
    print('add_words:           ', add_words[sid], end='\n\n', file=f3)
    print('before_Conj:        ', uns[sid*2], end='\n\n', file=f3)
    print('after_Conj:         ', uns[sid*2+1], end='\n\n', file=f3)
    print('\n\n\n', file=f3)
    
print(cnt1, cnt2, cnt0, cntn)