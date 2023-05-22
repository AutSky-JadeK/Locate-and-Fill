f1 = open('test-bertcrf.txt', 'r')
f2 = open('test-becky-bertcrf.txt', 'r')

cnt = 0

for i in range(53063):
    line1 = f1.readline()
    line2 = f2.readline()
    if line1 != line2:
        cnt += 1

print(cnt)