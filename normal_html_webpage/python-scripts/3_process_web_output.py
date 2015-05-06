
fdout = open("dataset_corrected.csv","w")
fdout.write("id,id_sub,is_directive,type,path,text:\n")




loops = 0 #put 0 for loop until end (infinite)

myset = {}


with open("merged.csv") as fdmerged:
	i = 1
	for line in fdmerged:
		if i>1:
			L = line.split(",",maxsplit=3)

			if L[0] not in myset.keys():
				myset[L[0]] = {L[1]:L[2][:-1]}
			else:
				if L[1] not in myset[L[0]].keys():
					myset[L[0]][L[1]] = L[2][:-1]
				else:
					print('myError: esto no deberia pasar, se repitió un id-subId - verificar merged.csv (el archivo de input)')
			
		i+=1


differentValueCount = 0
sameValueCount = 0
othernum = 0
with open("../dataset_withID_with_phrases_with-IsDirective-Info.csv") as fdDataset:
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

			if theid in myset.keys() and thesubid in myset[theid]:
				if thedirectivevalue != myset[theid][thesubid]:
					differentValueCount += 1
				else:
					sameValueCount += 1
				valueToWrite = myset[theid][thesubid]
			else:
				othernum += 1
				valueToWrite = thedirectivevalue

			fdout.write(','.join([line_splitted[0],line_splitted[1],valueToWrite,line_splitted[3],line_splitted[4],line_splitted[5]]))


		i += 1

print(str(differentValueCount) + ' values were changed.')
print(str(sameValueCount) + ' values left the same as before because the new value was the same as the old.')
print(str(othernum) + ' is the other num.')
lenn=0

print('size of set:'+str( sum(len(v) for v in myset.values() )) )