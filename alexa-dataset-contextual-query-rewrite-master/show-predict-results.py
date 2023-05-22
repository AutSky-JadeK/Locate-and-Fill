f1 = open('test-alexa.txt', 'r', encoding='utf-8')
f3 = open('predict_results_alexa.txt', 'r', encoding='utf-8')
f2 = open('show-alexa-predict-results.txt', 'w', encoding='utf-8')

while True:
	line = f1.readline()
	line = line.strip()
	line2 = f3.readline()
	line2 = line2.strip()
	if line == '':
		break
	pts = line.split('\t\t')
	pts2 = line2.split('\t\t')
	for utt in pts[:-2]:
		print(utt, file=f2)
	print('', file=f2)
	print(pts[-2], file=f2)
	print('', file=f2)
	print(pts2[-1], file=f2)
	print('', file=f2)
	print(pts[-1], file=f2)
	print('\n\n', file=f2)