from transformers import pipeline

f1 = open('tomask-filled-by-human.txt', 'r', encoding='utf-8')
f2 = open('after-bert.txt', 'w', encoding='utf-8')

unmasker = pipeline('fill-mask', model='bert-base-uncased')

while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
        '''
    pts2 = line.split(' ')
    '''
    if line.find('[MASK]') != -1:
        li = unmasker(line)
        line = line.replace('[MASK]', li[0]['token_str'])
        '''
    pts = line.split(' ')
    line = ''
    flag = False
    for i in range(len(pts)):
        if flag == False:
            if i != 0:
                line = line + ' '
            line = line + pts[i]
        else:
            flag = False
        if pts2[i] == '[MASK]':
            flag = True
            '''
    print(line, file=f2)