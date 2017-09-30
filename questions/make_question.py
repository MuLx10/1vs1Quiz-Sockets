file_name = 'ques.psv'
file_name_out = 'question.psv'

f = open(file_name,'r')
fo = open(file_name_out,'w')

string = {'a':0,'b':1, 'c':2, 'd':3}
while True:

	line = f.readline().strip('\n')
	if not line:
		break
	line = line.split('|')
	if line[-1] in "abcd":
		line[-1] = str(string[line[-1]])
	ques = ':s:'+':'.join(line[:-1])+":e:"+"|"+line[-1]+'\n'
	fo.write(str(ques))

fo.close()
f.close()
