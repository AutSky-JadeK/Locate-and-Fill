#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy  
import json


# In[2]:


def find_lcseque(s1, s2):   
    #print(s1)
    #print(s2)
     # 生成字符串长度加1的0矩阵，m用来保存对应位置匹配的结果 
    m = [ [ 0 for x in range(len(s2)+1) ] for y in range(len(s1)+1) ]   
    # d用来记录转移方向 
    d = [ [ None for x in range(len(s2)+1) ] for y in range(len(s1)+1) ]   

    for p1 in range(len(s1)):   
        for p2 in range(len(s2)):   
            if s1[p1] == s2[p2]:            #字符匹配成功，则该位置的值为左上方的值加1 
                m[p1+1][p2+1] = m[p1][p2]+1  
                d[p1+1][p2+1] = 'ok'            
            elif m[p1+1][p2] > m[p1][p2+1]:  #左值大于上值，则该位置的值为左值，并标记回溯时的方向 
                m[p1+1][p2+1] = m[p1+1][p2]   
                d[p1+1][p2+1] = 'left'            
            else:                           #上值大于左值，则该位置的值为上值，并标记方向up 
                m[p1+1][p2+1] = m[p1][p2+1]     
                d[p1+1][p2+1] = 'up'           
    (p1, p2) = (len(s1), len(s2))   
    s = []   
    while m[p1][p2]:    #不为None时 
        c = d[p1][p2]  
        if c == 'ok':   #匹配成功，插入该字符，并向左上角找下一个 
            s.append(s1[p1-1])  
            p1-=1  
            p2-=1   
        if c =='left':  #根据标记，向左找下一个 
            p2 -= 1  
        if c == 'up':   #根据标记，向上找下一个 
            p1 -= 1  
    s.reverse()   
    return ' '.join(s),m,d


# In[3]:


def add_label(A,B,m,d): #A original, B ground truth
    label = [ 'O' for _ in range(len(A))]  
    (p2, p1) = (len(A), len(B)) 
    flag=0# 1:上一次是left，2：上一次是up，0：上一次ok,3:复合操作
    segment=[]#正在被label的ner的index
    tmps = []
    while m[p1][p2]:    #不为None时 
        c = d[p1][p2]  
        if c == 'ok':  
            if flag==1 or flag==2:
                flag=0
                segment=[]
            if flag==3:
                for i in segment:
                    label[i]='REP'
                flag=0
            p1-=1  
            p2-=1
        if c =='left':  #根据标记，向左找下一个 
            if flag==0:
                #label[p2-1]='INS'
                segment.append(p2-1)
                flag=1
            if flag==2:
                flag=3
                segment.append(p2-1)
            if flag==3:
                segment.append(p2-1)
            p2 -= 1  
        if c == 'up':   #根据标记，向上找下一个 
            if flag==0:
                label[p2-1]='INS'
                flag=2
                tmps = [[]] + tmps
            if flag==1:
                flag=3
                segment.append(p2-1)
            if flag==3:
                segment.append(p2-1)
            p1 -= 1  
            tmps[0] = [B[p1]] + tmps[0]
    return label, tmps


# In[4]:


def add_bio(label):
    label_bio=[]
    flag=0
    for l in label:
        if l=='REP':
            if flag==0:
                label_bio.append('B-'+l)
                flag=1
            else:
                label_bio.append('I-'+l)
        elif l=='INS':
            label_bio.append('B-'+l)
            flag=0
        else:
            label_bio.append('O')
            flag=0
    #print(label_bio)
    return label_bio

def front_to_behind(label):
    res = label[:-1]
    for i in range(len(res)):
        if label[i+1] == 'B-REP' or label[i+1] == 'I-REP':
            res[i] = label[i+1]
        elif label[i] == 'B-INS':
            res[i] = label[i]
        else:
            res[i] = 'O'
    return res


'''
# In[5]:


testa = '[CLS] what made anna get into politics ? [SEP]'
testb = '[CLS] if what if made anna ella carroll get into politics ? [SEP]'
A=testa .split(' ')
B=testb .split(' ')


# In[6]:


lcs,m,d=find_lcseque(B,A)


# In[7]:


print(lcs)


# In[8]:


label=add_label(A,B,m,d)
print(label)


# In[9]:


label=add_bio(label)
print(label)


# In[10]:
'''

id_now = 0

def cona(lis):
    sn_contact = ''
    for i in range(len(lis)):
        if i != 0:
            sn_contact += ' '
        sn_contact += lis[i]
    return sn_contact

def getsns(sen, label):
    sns = []
    sn = []
    be_replaced = []
    s_with_mask = []
    for i in range(len(sen)):
        if label[i] == 'O':
            if sen[i] != '[EOS]':
                for j in range(len(sns)):
                    sns[j].append(sen[i])
                s_with_mask.append(sen[i])
                sn.append(sen[i])
        elif label[i] == 'B-INS':
            sns.append(sn)
            sns[-1] = sns[-1] + ['<extra_id_0>', '(', ')']
            s_with_mask.append('[MASK_i]')
            if sen[i] != '[EOS]':
                for j in range(len(sns)):
                    sns[j].append(sen[i])
                sn.append(sen[i])
                s_with_mask.append(sen[i])
        elif label[i] == 'B-REP' or label[i] == 'I-REP':
            be_replaced.append(sen[i])
            if label[i+1] != 'I-REP':
                for j in range(len(sns)):
                    sns[j] = sns[j] + be_replaced
                sns.append(sn)
                sns[-1] = sns[-1] + (['<extra_id_0>', '('] + be_replaced + [')'])
                sn = sn + be_replaced
                s_with_mask.append('[MASK_r]')
                be_replaced = []
    return sns, s_with_mask
        

dataset_name = 'mudoco_test'

with open(dataset_name + '.txt',"r",encoding="utf-8") as f_read:
    content=f_read.readlines()


# In[11]:
fo_1 = open(dataset_name + '-becky-prompt-5571-T5.json', 'w', encoding='utf-8')
fo_2 = open(dataset_name + '-becky-prompt-5571-T5-ids.txt', 'w', encoding='utf-8')
fo_3 = open(dataset_name + '-becky-prompt-5571-T5-inputs.txt', 'w', encoding='utf-8')
fo_4 = open(dataset_name + '-becky-bertcrf.txt', 'w', encoding='utf-8')
fo_5 = open(dataset_name + '-with-mask-becky-prompt.txt', 'w', encoding='utf-8')
fo_6 = open(dataset_name + '-direct-5571-T5.json', 'w', encoding='utf-8')
fo_7 = open(dataset_name + '-direct-5571-T5-inputs.txt', 'w', encoding='utf-8')

cnt_not_equal = 0

for line in content:
    line = line.strip()
    pts = line.split('\t\t')
    testa='[CLS] '+pts[-2]+' [SEP]'
    testb='[CLS] '+pts[-1]+' [SEP]'
    A=testa.split(' ')
    B=testb.split(' ')
    lcs,m,d=find_lcseque(B,A)
    #print(lcs)
    label, tmps=add_label(A,B,m,d)
    #print(label)
    label=add_bio(label)
    label=front_to_behind(label)
    prta = A[1:]
    prta[-1] = '[EOS]'
    for i in range(len(prta)):
        print(prta[i] + '\t' + label[i], file = fo_4)
    sns, s_with_mask = getsns(prta, label)
    
    lin = ''
    for sen in pts[:-2]:
        if lin != '':
            lin = lin + ' [SEP] '
        lin = lin + sen
    
    #print(id_now+1)
    #print(sns)
    #print(tmps)
    '''
    if len(tmps) != len(sns):
        print(pts[-2])
        print(pts[-1])
        print(sns)
        print(tmps)
        print("")
        cnt_not_equal += 1
        id_now += 1
        continue
        '''
        
    for i in range(len(sns)):
        prt={'text': lin + ' [SEP] ' + cona(sns[i]),
        'summary': cona(tmps[i])}
        print(json.dumps(prt), file=fo_1)
        print(id_now, file=fo_2)
        print(prt['text'], file=fo_3)
    
    prt2={'text': lin + ' [SEP] ' + pts[-2],
        'summary': pts[-1]}
    print(json.dumps(prt2), file=fo_6)
    print(prt2['text'], file=fo_7)
        
    print("", file = fo_4)
    print(line + '\t\t' + cona(s_with_mask), file = fo_5)
    
    id_now += 1
    
#print(cnt_not_equal)

# In[ ]:




