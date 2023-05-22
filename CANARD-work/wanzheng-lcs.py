import json

def clean(s):
    res = ''
    for i in range(len(s)):
        if i+1 < len(s) and s[i] == ' ' and (s[i-1] == "'" and s[i+1] == 's') and (i+2 >= len(s) or s[i+2] == ' ') and (i-2 < 0 or s[i-2] == ' '):
            continue
        if i > 1 and (s[i] == '!' or s[i] == '?' or s[i] == "'" or s[i] == ",") and s[i-1] != ' ':
            res = res + ' '
        res = res + s[i]
    return res

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
    return ''.join(s),m,d
    
f1 = open('test-becky-ner-5571-T5-outputs-wanzheng.txt', 'r', encoding='utf-8')
f2 = open('test-becky-ner-5571-T5-outputs.txt', 'r', encoding='utf-8')
f3 = open('test-becky-ner-5571-T5-outputs-wanzheng-lcs.txt', 'w', encoding='utf-8')
cnt = 0

while True:
    ss1 = f1.readline()
    ss1 = ss1.strip()
    ss2 = f2.readline()
    ss2 = ss2.strip()
    
    lcs, _, __ = find_lcseque(clean(ss1),clean(ss2))
    
    print(lcs, file=f3)
    
    cnt += 1
    if cnt == 6569:
        break