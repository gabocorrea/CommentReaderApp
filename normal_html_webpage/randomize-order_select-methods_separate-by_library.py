"""	Lee dataset_withID_with_phrases_with-IsDirective-Info ----- ValuesModifiedAccordingWithWebappOutput.csv
	un .csv que tiene header id,id_sub,is_directive,type,path,text
	
	cada vez que encuentra una frase que comienza con @link (en su campo text de .csv)
	une esa frase con la anterior.
	Las frases se iran uniendo de arriba hacia abajo si hay varias frases contiguas que comienzan con @link,
	es decir sera la frase 1 con la 2, luego la resultante entre estas y la frase 3, etc.
	la frase resultante que fue unida, quedara con valor
	is_directive==1 si al menos una de ellas tenia ese valor... quedara con valor 
	is_directive==2 si al menos una de ellas tenia ese valor y ninguna tenia valor 1...quedara con valor
	is_directive==3 si al menos una de ellas tenia ese valor y ninguna tenia valor 2 ni 1...quedara con valor
	is_directive==0 si todas ellas tienen valor 0.

	Escribe los resultados en dataset_withID_with_phrases_with-IsDirective-Info -- @link_fixed.csv
	"""
import sys,os,collections

amarillo='1'
azul='2'
naranjo='3'

def calculateDirectiveValue(lastval, nowval):
	if lastval == nowval:
		return nowval
	elif lastval == amarillo or nowval == amarillo:
		return amarillo
	elif lastval==azul or nowval==azul:
		return azul
	elif lastval==naranjo or nowval==naranjo:
		return naranjo

def correctPath(thepath,linesDeletedInCurrentId):
	s=thepath
	if s[-4:-3]=="#":
		n=int(s[-3:])
		j=3
	elif s[-3:-2]=="#":
		n=int(s[-2:])
		j=2
	elif s[-2:-1]=="#":
		n=int(s[-1:])
		j=1
	else:
		sys.error('this should not happen')
	return s[:-j]+str(n-linesDeletedInCurrentId)

fdout = open("dataset_withID_with_phrases_with-IsDirective-Info -- @link_fixed.csv","w")
#fdout = open("fix @link problem.csv","w")
fdout.write("id,id_sub,is_directive,type,path,text\n")


loops = 0 #put 0 for loop until end (infinite)



lastInfo=None
allCommentsDict = collections.OrderedDict()
linesDeletedInCurrentId=None
with open("dataset_withID_with_phrases_with-IsDirective-Info.csv") as fdDataset:
#with open("fix @link problem -- test-program-with-this.csv") as fdDataset:
	i = 1
	for line in fdDataset:

		if i>1:
			if loops<1 and i%10000==0:
				print(i)
			if loops>=1 and i>=loops:
				break

			
			line_splitted = line.split(",",maxsplit=5)

			theid = line_splitted[0]
			thesubid = line_splitted[1]
			thedirectivevalue = line_splitted[2]
			thetype = line_splitted[3]
			thepath = line_splitted[4]
			text = line_splitted[5]
			if theid not in allCommentsDict.keys():
				allCommentsDict[theid] = collections.OrderedDict()
				linesDeletedInCurrentId=0
			if '@link' in text[:7]:#si se encuentra ese string mas o menos al principio de text...then:
				linesDeletedInCurrentId+=1
				allCommentsDict[lastInfo['theid']][lastInfo['thesubid']]['text'] = allCommentsDict[lastInfo['theid']][lastInfo['thesubid']]['text'][:-1] + text #el :-1 es para no incluir el newline
				allCommentsDict[lastInfo['theid']][lastInfo['thesubid']]['directivevalue'] = calculateDirectiveValue(lastInfo['thedirectivevalue'], thedirectivevalue)
			else:
				if linesDeletedInCurrentId==None:
					sys.error()#should never happen
				lastInfo = {'theid':theid,'thesubid':str(int(thesubid)-linesDeletedInCurrentId),'thedirectivevalue':thedirectivevalue,'text':text}
				allCommentsDict[theid][str(int(thesubid)-linesDeletedInCurrentId)] = {'text':text,'directivevalue':thedirectivevalue,'type':thetype,'path':correctPath(thepath,linesDeletedInCurrentId)}

		i+=1

			
for theid in allCommentsDict.keys():
	for thesubid in allCommentsDict[theid]:
		fdout.write(','.join( (theid,thesubid,allCommentsDict[theid][thesubid]['directivevalue'],allCommentsDict[theid][thesubid]['type'],allCommentsDict[theid][thesubid]['path'],allCommentsDict[theid][thesubid]['text'])) )