from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('/root/ParlAI4/stanford-corenlp-4.4.0')
exceptions = ['your','my','yourself','myself','you','i','hers','yours','mine','theirs']

def haveletternum(s):
    flag = False
    for i in s:
        if i.isalnum() :
            flag = True
    return flag

def parse_utt_o(sent):
    a_parse = nlp.parse(sent)
    a_parses = a_parse.split('\n')
    parse_res = []
    for cont in a_parses:
        asp = cont.split('(')
        phrase = [asp[1].strip()]
        for c in asp[2:]:
            phrase.append(c.strip().strip(')').split(' '))
        parse_res.append(phrase)
    return parse_res

def parse_utt(sent):
    a_parse = nlp.parse(sent)
    a_parses = a_parse.split('\n')
    parse_res = []
    for cont in a_parses:
        asp_o = cont.split('(')
    
        if len(asp_o) == 2:
            symbs = asp_o[1:]
        
        if cont.find(')))') == -1 or haveletternum(cont) == False or asp_o[1].find(')') == -1:
            cont_m = cont
        else:
        #print(cont)
            cont_m = '(' + symbs[-1] + cont
            cont_m.strip()
        #print(cont_m)
        asp = cont_m.split('(')
        phrase = [asp[1].strip()]

        for c in asp[2:]:
            phrase.append(c.strip().strip(')').split(' '))
        parse_res.append(phrase)
    return parse_res
        

def add_mask(sent):
    output_sent = ""
    words_ini = []
    
    pos_tag = nlp.pos_tag(sent)
    for it in pos_tag:
        words_ini.append(it[0])
    words = words_ini.copy()
   
    dict_pars = {}
    dict_pos = {}
    symbs_all = []
    

    num_p = 0
    flag_p = False
    sub_str = []
    sub_sent = []

    for it in pos_tag:
        dict_pos[num_p] = it[-1]
        if it[-1] == '.':
            if num_p != len(pos_tag) - 1:
                flag_p = True
            sub_str.append(it[0])                
        num_p = num_p + 1
    #print(sub_str)
    if flag_p == True:
        head = 0
        tail = len(sent)
        sub_sent.append(sent[head:sent.find(sub_str[0], head, tail)+1])
        head = sent.find(sub_str[0], head, tail)+1
        for g in sub_str[1:]:
            tail = sent.find(g, head, tail)
            #print(tail)
            sub_sent.append(sent[head:tail+1])
            head = tail+1
            tail = len(sent)
            #print(head)
                #tail = len(sent)
        if tail != len(sent)-1:
            #print(head)
            sub_sent.append(sent[head:len(sent)])
    #print(sub_sent)  
    if '' in sub_sent:
        sub_sent.remove('')
    a_parses = []
    #print(len(sub_sent))
    if len(sub_sent) > 0:
        for s in sub_sent:
            #print(nlp.parse(s))
            #print(len(nlp.parse(s).split('\n')))
            for cont in nlp.parse(s).split('\n'):
                a_parses.append(cont)
    else: 
        a_parses = nlp.parse(sent).split('\n')
    #print(a_parses)
    num = 0
    for cont in a_parses:
        asp_o = cont.split(' (')
        #set_asp = set(asp_o)
    #print(set_asp)
        if '' in asp_o:
            asp_o.remove('')
        for it in asp_o:
            if '  ' in it or it == ' ':
            #print(' 'in it)
                asp_o.remove(it)
        for it in asp_o:
            if len(asp_o) > 1 and len(it.split(' ')) == 1:
                symbs_all.append(it)
            elif len(asp_o) == 1 and haveletternum(it) == True:
                symbs_all.append(it)
            elif haveletternum(it) == False:
                symbs_all.append(it[0])
        for it in asp_o: 
            if len(it.split(' ')) > 1 :
                dict_pars[num] = symbs_all[-1]
                dict_pos[num] = it.split(' ')[0]
                #dict_pos[num] = pos_tag[num][1]
                num = num + 1
            elif haveletternum(it) == False:
                dict_pars[num] = symbs_all[-1]
                dict_pos[num] = symbs_all[-1] 
                num = num + 1
    
   
    
    #rule: if after/before in the end of utt，add [mask]
    flag_end_1 = False
    flag_end_2 = False
    if words_ini[-1] == 'after' or words_ini[-1] == 'before' or words_ini[-1].lower() == 'what' or  words_ini[-1].lower() == 'why' or words_ini[-1].lower() == 'how' :
        flag_end_1 = True
    elif len(words_ini) > 1 :
        if words_ini[-2] == 'after' or words_ini[-2] == 'before' or words_ini[-2].lower() == 'what' or  words_ini[-2].lower() == 'why' or words_ini[-2].lower() == 'how' and haveletternum(words_ini[-1]) == False:
            flag_end_2 = True 
    
    for i in range(len(words_ini)):
            
        #rule: replace pronouns
        
        #rule: their house -> the house of kate and ben
        if dict_pos[i] == 'PRP$' and dict_pars[i] == 'NP'  and dict_pars[i+1] == 'NP' and words_ini[i].lower() not in exceptions:
            #print(words_ini[i])
            words_ini.pop(i)
            words_ini.insert(i,'the')
            #print(words_ini[i])
    
        
        if dict_pos[i] == 'PRP' and words_ini[i].lower() != 'you' and words_ini[i].lower() != 'i' and words_ini[i].lower() != 'me':
            #print(i)
            #print(words_ini)
            #print("pronoun: ",words_ini[i])
            #print(dict_pos)
            words.insert(i+abs(len(words_ini)-len(words)),'[MASK_r]')
            words.pop(i+abs(len(words_ini)-len(words)))
        
        
        #rule: deal with 'that', 'this','these','those'
        elif words_ini[i].lower() == 'this' or words_ini[i].lower() == 'that' or words_ini[i].lower() == 'these' or words_ini[i].lower() == 'those' and dict_pos[i] == 'DT':
            #i find that book interesting (insert)
            if i+1 < len(dict_pars) and dict_pars[i+1] == 'NP':
                m = i
                while m < len(dict_pars) and dict_pars[m] == 'NP':
                    m = m + 1
                words.insert(m+abs(len(words_ini)-len(words)),'[MASK_i]')
            else: #i find that interesting
                #print("this, that: ", words_ini[i])
                words.insert(i+abs(len(words_ini)-len(words)),'[MASK_r]')
                words.pop(i+abs(len(words_ini)-len(words)))
                
            
                
        #rule: deal with noun with "the"
        elif words_ini[i].lower() == 'the' and dict_pars[i] == 'NP':
        
            j = i
            while j < len(dict_pars) and dict_pars[j] == 'NP':
                
                j = j + 1
            
            if words[i+abs(len(words_ini)-len(words))] != words_ini[i]:

                
                words.insert(i+abs(len(words_ini)-len(words)),words_ini[i])
                words.pop(i+abs(len(words_ini)-len(words)))
            words.insert(j+abs(len(words_ini)-len(words)),'[MASK_i]')
        
        #rule: deal with else
        elif words_ini[i].lower() == 'else' and words[0] != '[MASK_i]':
            words.insert(0,'[MASK_i]')
            words.insert(1,',')
    
    #rule: deal with other and another
    if 'other' in words or 'another' in words and words[0] != '[MASK_i]':
        words.insert(0,'[MASK_i]')
        words.insert(1,',')
    if flag_end_1 == True:
        words.insert(len(words),'[MASK_i]')
    if flag_end_2 == True: 
        words.insert(len(words)-1,'[MASK_i]')
        
    for w in words:
        output_sent += w + " "
    return output_sent

#read data from the file:
f1 = open('/root/test.txt', 'r', encoding='utf-8')
pts_all = []
for line in lines:
    line = line.strip()
    pts = line.split('\t\t')
    pts_all.append(pts)

#implement the rewriting
write_lines = []
for i in range(len(pts_all)):
    #print(i)
    dial = pts_all[i]
    mask_utt =  add_mask(dial[-2])
    write_line = lines[i].strip() + '\t\t' + mask_utt + '\n'
    write_lines.append(write_line)

#output the rewriting results into a file   
with open('result_output.txt','w') as f:
    for cont in write_lines:
        f.write(cont)