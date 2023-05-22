import json

f1 = open('cqr_kvret_test_public.json', 'r', encoding='utf-8')
f2 = open('alexa_test.txt', 'w', encoding='utf-8')

dic = json.load(f1)

sumdis, avedis, cnt = 0, 0, 0
diss = {}
sumlen, avelen, cntdia = 0, 0, 0
extra_wds = {}
extra_wds_list = []

def cona(lis):
    sn_contact = ''
    for i in range(len(lis)):
        if i != 0:
            sn_contact += ' '
        sn_contact += lis[i]
    return sn_contact

def is_biaodian(tk):
    if tk.isdigit() == False and tk.isalpha() == False and tk != ' ':
        return True
    return False
    
'''
def is_dig_or_alp:
    if tk.isdigit() == True or tk.isalpha() == True:
        return True
    return False
'''

def addblank(ss):
    res = ''
    for i in range(len(ss)):
        if i >= 1 and is_biaodian(ss[i]) and ss[i-1] != ' ':
            res += ' '
        elif i >= 1 and is_biaodian(ss[i-1]) and ss[i] != ' ':
            res += ' '
        res += ss[i]
    return res.strip()

for sam in dic:
    sumlen += len(sam['dialogue'])
    cntdia += 1
    for i in range(0, len(sam['dialogue'])):
        if 'reformulation' in sam['dialogue'][i] and sam['dialogue'][i]['reformulation']['reformulated_utt'] != None:
            pts = []
            for j in range(0, i+1):
                pts.append(addblank(sam['dialogue'][j]['data']['utterance'].strip()))
            pts[-1] = addblank(sam['dialogue'][i]['reformulation']['reformulated_utt'].strip())
            prt = ''
            for j in range(len(pts)):
                if j != 0:
                    prt = prt + '\t\t'
                prt = prt + pts[j]
            print(prt, file=f2)
            wds = []
            #print(pts)
            for sen in pts:
                wds.append(sen.split(' '))
            new_wd = []
            for wd in wds[-1]:
                if wd not in wds[-2]:
                    new_wd.append(wd)
            dis_new_wd = []
            for i in range(-3, -len(pts)-1, -1):
                for wd in wds[i]:
                    while wd in new_wd:
                        new_wd.remove(wd)
                        dis_new_wd.append([wd, -i-2])
            for wd in new_wd:
                dis_new_wd.append([wd, 0])
                if wd in extra_wds.keys():
                    extra_wds[wd] += 1
                else:
                    extra_wds[wd] = 1
                    extra_wds_list.append(wd)
            for pir in dis_new_wd:
                if pir[1] != 0:
                    sumdis += pir[1]
                    cnt += 1
                if pir[1] in diss.keys():
                    diss[pir[1]] = diss[pir[1]] + 1
                else:
                    diss[pir[1]] = 1
    #break
    
'''
avelen = sumlen / cntdia
print('avelen', avelen)
            
avedis = sumdis / cnt
print('avedis', avedis)
for ke in diss:
    print(ke, diss[ke])
    
    
print('\n\n\n')

extra_wds_list = sorted(extra_wds_list, key=lambda x: extra_wds[x], reverse=True)

for wd in extra_wds_list:
    print(wd, extra_wds[wd])
'''