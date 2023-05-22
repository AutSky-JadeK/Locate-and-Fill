import json

def getlcs(sa, sb):
    la = []
    lb = []
    
    for i in range(len(sa)):
        la.append(False)
    for i in range(len(sb)):
        lb.append(False)
        
    ssa = ['<begin>'] + sa
    ssb = ['<begin>'] + sb
    
    LCS = []
    DIR = []
    
    
    
    for i in range(len(ssa)):
        LCS.append([])
        DIR.append([])
        for j in range(len(ssb)):
            LCS[-1].append(0)
            DIR[-1].append(0)
            
    for i in range(len(ssa)):
        for j in range(len(ssb)):
            if i!=0 and j!=0:
                if ssa[i] == ssb[j]:
                    LCS[i][j] = LCS[i-1][j-1] + 1
                    DIR[i][j] = 0
                else:
                    LCS[i][j] = max(LCS[i-1][j], LCS[i][j-1])
                    if LCS[i-1][j] >= LCS[i][j-1]:
                        DIR[i][j] = 1
                    else:
                        DIR[i][j] = 2
                        
    i = len(ssa) - 1
    j = len(ssb) - 1
    while i!=0 and j!=0:
        if ssa[i] == ssb[j]:
            la[i-1] = True
            lb[j-1] = True
        if DIR[i][j] == 0:
            i -= 1
            j -= 1
        elif DIR[i][j] == 1:
            i -= 1
        else:
            j -= 1
            
    lsta = []
    for i in range(len(la)):
        if la[i] == False:
            if i == 0 or la[i-1] == True:
                lsta.append([])
            lsta[-1].append(i)
    
    if 0 not in lsta[0]:
        lsta = [[-1]] + lsta
    if len(la) - 1 not in lsta[-1]:
        lsta =  lsta + [[len(la)]]
    
    lstb = []
    for i in range(len(lb)):
        if lb[i] == False:
            if i == 0 or lb[i-1] == True:
                lstb.append([])
            lstb[-1].append(i)
            
    if 0 not in lstb[0]:
        lstb = [[-1]] + lstb
    if len(lb) - 1 not in lstb[-1]:
        lstb =  lstb + [[len(lb)]]
            
    return la, lb, lsta, lstb
    
def getpoints(lst, d, l):
    ll = lst[d-1][-1] + 1 if d > 0 else 0
    lr = lst[d][0] - 1
    rl = lst[d][-1] + 1
    rr = lst[d+1][0] - 1 if d < len(lst) - 1 else l - 1
    return ll, lr, rl, rr
    
def is_replaced(sa, sb, da, db, la, lb, lsta, lstb):
    if da >= len(lsta) or db >= len(lstb):
        return False
    a_ll, a_lr, a_rl, a_rr = getpoints(lsta, da, len(sa))
    b_ll, b_lr, b_rl, b_rr = getpoints(lstb, db, len(sb))
    
    if a_lr - a_ll > b_lr - b_ll:
        a_ll += ((a_lr - a_ll) - (b_lr - b_ll))
    else:
        b_ll += ((b_lr - b_ll) - (a_lr - a_ll))
        
    if a_rr - a_rl > b_rr - b_rl:
        a_rr -= ((a_rr - a_rl) - (b_rr - b_rl))
    else:
        b_rr -= ((b_rr - b_rl) - (a_rr - a_rl))
    
    if sa[a_ll:a_lr+1] == sb[b_ll:b_lr+1] and sa[a_rl:a_rr+1] == sb[b_rl:b_rr+1]:
        return True
    return False

def getner(sa, sb):
    la, lb, lsta, lstb = getlcs(sa, sb)
    print(lsta, lstb)
    da = 0
    ner_label = []
    for i in range(len(sa) + 1):
        ner_label.append('O')
    for db in range(len(lstb)):
        flag = is_replaced(sa, sb, da, db, la, lb, lsta, lstb)
        for j in range(len(lsta[da])):
            if flag == True:
                if j == 0:
                    ner_label[lsta[da][j]] = 'B-REP'
                else:
                    ner_label[lsta[da][j]] = 'I-REP'
        if flag == False:
            sumnot = 0
            for j in range(db):
                sumnot += len(lstb[j]) if (lstb[j][0] != -1 and lstb[j][0] != len(lb)) else 0
            leftlength = lstb[db][0] - sumnot
            if leftlength < 0:
                leftlength = 0
            ok = False
            cntlabel = 0
            getinsert = False
            if cntlabel == leftlength:
                ok = True
            for j in range(len(la)):
                if la[j] == True:
                    cntlabel += 1
                    if ok == True:
                        if ner_label[j] == 'O':
                            ner_label[j] = 'B-INS'
                        getinsert = True
                        break
                    if cntlabel == leftlength:
                        ok = True
            if getinsert == True:
                if ner_label[-1] == 'O':
                    ner_label[-1] = 'B-INS'
        if flag == True:
            da += 1
    return ner_label


testa = 'are there any other interesting aspects about this article ?'
testb = 'what are interesting aspects relating to the rise to notability other than the album incorporating r&b influences ?'

print(testa)
print(testb)
print(getner(testa.split(' '), testb.split(' ')))