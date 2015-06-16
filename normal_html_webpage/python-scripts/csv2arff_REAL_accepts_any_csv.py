"""Converts a .csv file to a .arff file. Output file has the same name as input file, but with the extension changed to .arff"""

"""for now it only works for 2 columns: text,number       fix mysplit to make it work for more columns"""

import re
import csv,sys

STRING_DELIMITER='¿'


def mysplit(astring, splitchar, maxsplit, ignoresplitcharacter):
	p1=astring
	p2=splitchar
	p3=maxsplit
	p4=ignoresplitcharacter

	L=[]
	pos=p1.find(p4)
	if pos<=-1:
		return p1.split(p2,p3)
	else:
		pos2=p1.find(p4,pos+1)
		L.append( p1[pos:pos2+1] )
		L.append( p1[ p1.find(',',pos2) :  ] )
		return L


if len(sys.argv)<=1:
	print('\nUsage: csv2arff_REAL_accepts_any_csv.py <input.csv> type1 type2 type3 ...\n')
	sys.exit()

with open(sys.argv[1]) as filein:
	for line in filein:
		firstLine = line
		break

	firstLineWords = firstLine.split(',')
	num_of_columns = len(firstLineWords)

	firstLineWords[-1] = firstLineWords[-1][:-1] #take away the newline character

	if num_of_columns!=len(sys.argv)-2:
		print('\nlist of types in input must match number of columns of csv file')
		print('Usage: csv2arff_REAL_accepts_any_csv.py <input.csv> type1 type2 type3 ...\n')
		sys.exit()



	with open(sys.argv[1][:-3]+'arff',"w") as fdout:
		fdout.write("% 1. Title: arff file created from "+ sys.argv[1] +"\n\n")
		fdout.write("@RELATION \""+sys.argv[1][:-3]+"arff\"\n\n")

		for i in range(num_of_columns):
			fdout.write("@ATTRIBUTE "+firstLineWords[i]+ " "+ sys.argv[i+2]  +"\n")
		fdout.write("\n@DATA\n")


		for line in filein:
			### esto no es necesario ###row = mysplit(line,',', num_of_columns-1, STRING_DELIMITER)
			fdout.write(line)