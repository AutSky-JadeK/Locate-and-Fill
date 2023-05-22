datafile = 'train'

f1 = open(datafile + '.csv', 'r', encoding='utf-8')
f2 = open(datafile + '-bertcrf.txt', 'w', encoding='utf-8')

entries = f1.read().strip().split("\n\n")
for entry in entries:
    lines = entry.splitlines()
    lines = lines + ['[EOS]' + '\t' + 'O']
    flag = False
    beftag = ''
    for line in lines:
        bef = ''
        pieces = line.strip().split()
        if pieces[-1] == 'B_REP':
            pieces[-1] = 'B-REP'
        elif pieces[-1] == 'I_REP':
            pieces[-1] = 'I-REP'
        elif pieces[-1] == 'E_REP':
            pieces[-1] = 'I-REP'
        elif pieces[-1] == 'E_REP':
            pieces[-1] = 'I-REP'
        elif pieces[-1] == 'B_BEF':
            pieces[-1] = 'B-INS'
        if flag == True:
            bef = pieces[-1]
            pieces[-1] = 'B-INS'
            flag = False
        if pieces[-1] == 'B_AFT' or bef == 'B_AFT' or pieces[-1] == 'B_TWO' or bef == 'B_TWO':
            flag = True
            if pieces[-1] == 'B_AFT':
                pieces[-1] = 'O'
            elif pieces[-1] == 'B_TWO':
                pieces[-1] = 'B-INS'
        if pieces[-1] == 'B-REP' or pieces[-1] == 'I-REP':
            if beftag != 'B-REP' and beftag != 'I-REP':
                pieces[-1] = 'B-REP'
            else:
                pieces[-1] = 'I-REP'
        print(pieces[0] + '\t' + pieces[-1], file=f2)
        beftag = pieces[-1]
    print('', file=f2)