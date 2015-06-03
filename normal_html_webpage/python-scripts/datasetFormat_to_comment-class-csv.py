filename='dataset_corrected_only_comments_and_manually_revised_subset'
fdout = open(filename+'_(only comments and class).csv','w')

linesNotCorrectlyFormated = 0
with open(filename+'.csv') as fdin:
	i=0
	for line in fdin:
		splitted = line.split(',',5)
		if len(splitted) == 6:
			if i<=0:
				fdout.write(splitted[5][:-1]+','+splitted[2]+'\n')
			else:
				fdout.write('¿'+splitted[5][:-1]+'¿,'+splitted[2]+'\n')
		else:
			linesNotCorrectlyFormated += 1
		i+=1

print('linesNotCorrectlyFormated='+str(linesNotCorrectlyFormated))