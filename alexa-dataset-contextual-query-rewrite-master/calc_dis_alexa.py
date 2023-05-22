import json

f1 = open('cqr_kvret_test_public.json', 'r', encoding='utf-8')

dic = json.load(f1)

sumdis, avedis, cnt = 0, 0, 0
diss = {}
sumlen, avelen, cntdia = 0, 0, 0
extra_wds = {}
extra_wds_list = []

for sam in dic:
    sumlen += len(sam['dialogue'])
    cntdia += 1
    for i in range(0, len(sam['dialogue'])):
        if 'reformulation' in sam['dialogue'][i] and sam['dialogue'][i]['reformulation']['reformulated_utt'] != None:
            pts = []
            for j in range(0, i+1):
                pts.append(sam['dialogue'][j]['data']['utterance'])
            pts[-1] = sam['dialogue'][i]['reformulation']['reformulated_utt']
            #print(pts)
            #break
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