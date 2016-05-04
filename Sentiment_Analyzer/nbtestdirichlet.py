import operator
__author__ = 'Sharmodeep Sarkar and Sarita Joshi'
#########################Importing Python Libraries############################
import sys,os
from math import log
import pickle
import re
from decimal import Decimal  # this gives more precision as compared to float

#data= []
PosTermProb = {}
PosLen = 0
NegTermProb = {}
NegLen = 0
Pp = 0 # class prior label positive
Pn = 0 # class prior  label negative
VocabLen =0
PosFiles = []
NegFiles = []
UnpredictableFiles = []
PredictTable = []			#Stores the filename storing the file, pos and neg scores
SortedPosProb = []
SortedNegProb = []
PosNegWeight = {}
NegPosWeight = {}
SmoothingProb = {}
smoothingParamater = 0

def readFile (testDir):
	global PosTermProb,NegTermProb,Pp,Pn,VocabLen,PosLen,NegLen,SortedNegProb,SortedPosProb,SmoothingProb,smoothingParamater
	print 'Read Model File'
	with open("model.txt",'r') as data_file:
		data = pickle.load(data_file)
	data_file.close()
	print len(data)
	PosTermProb = data[0]
	PosLen = data[1]
	NegTermProb = data[2]
	NegLen = data[3]
	Pp = data[4]
	Pn = data[5]
	VocabLen = data[6]
	SmoothingProb = data[7]
	smoothingParamater =  data[8]
	print len(PosTermProb) , '  ', len(NegTermProb) , '  ' , Pp, Pn
	print 'smoothingParamater is ', smoothingParamater
	filenames = os.listdir( testDir ) # List of filenames in the test dir
	testDir+='\\'
	predictClass ([testDir + f for f in filenames])
	


def predictClass (listOfFilenames):
	global PosFiles,NegFiles,PredictTable
	for filename in listOfFilenames:
		try:
			f=open( filename,'r')
		except:
			print "File Can't be read", f
			exit()
		input = f.read()
		f.close()
		# Removing punctuations from inputs (hyphens are retained)
		input = re.sub(ur"[^\w\d'\s-]+",' ',input)
		input = input.replace('\n', ' ')
		words = input.split()
		print "len of words --->>", len(words)
		posScore = getPosScore(words)
		negScore = getNegScore(words)
		data_format = (filename,posScore,negScore)
		formatted_content = '{:>2}\t\t{:>20}\t\t{:>10}'.format(*data_format)
		PredictTable.append(formatted_content)
		if (posScore>negScore):
			PosFiles.append(filename)
		if (posScore<negScore):
			NegFiles.append(filename)
		else:
			UnpredictableFiles.append(filename)
		print filename , " posScore  ", posScore, " negScore  ", negScore
	calcPercentage (len(listOfFilenames),len(PosFiles),len(NegFiles))    # TEST METHOD !!!!! CALCULATING % OF FILES IN EACH CLASS
	writePredictionFile ()


def getPosScore (lisOfWords):
	posScore = log(Pp)
	for word in lisOfWords:
		if word in SmoothingProb.keys():
			termNotInClassScore = (SmoothingProb[word] * smoothingParamater) / (PosLen+smoothingParamater)
			#print word, '  ', termNotInClassScore
			posScore += log(PosTermProb.get(word,termNotInClassScore))
	return posScore


def getNegScore (lisOfWords):
	negScore = log(Pn)
	for word in lisOfWords:
		if word in SmoothingProb.keys():
			termNotInClassScore = (SmoothingProb[word] * smoothingParamater) / (smoothingParamater+NegLen)
			negScore += log(NegTermProb.get(word,termNotInClassScore))		
	return negScore


# TEST METHOD !!!!!!!!
def calcPercentage(totalFiles,posFiles,negFiles):
	posFilePercentage = posFiles/(totalFiles*1.0)*100
	negFilePercentage = negFiles/(totalFiles*1.0)*100
	print 'totalFiles ', totalFiles
	print "Postive Files % = " , posFilePercentage
	print posFiles
	print "Negative Files % = ", negFilePercentage
	print negFiles


def writePredictionFile ():
	global PredictTable
	print ("Writing Prediction File ")
	output=open("prediction.txt",'w')
	i = 0
	output.write("List of Files in Test Directory with Pos and Neg Score based on Model File\n\n")
	output.write("Total Test Files ->" + str(len(PredictTable)) + '\n\n')
	table_header = ('FILENAME', 'POS_SCORE', 'NEG_SCORE')
	formatted_header = '{:>5}\t\t{:>25}\t\t{:>12}'.format(*table_header)
	output.write(formatted_header + '\n')
	while i < len(PredictTable):
		output.write(PredictTable[i] + '\n')
		i += 1
	output.write("Below is the segregated list of Positive and Negative files from Test Directory\n\n")
	output.write('Positive Files with Count ->' + str(len(PosFiles)) + "\n")
	for filename in PosFiles:
		output.write(filename)
		output.write ('\n')
	output.write('\n\n')
	output.write('Negative Files with Count ->' + str(len(NegFiles)) + "\n")
	for filename in NegFiles:
		output.write(filename)
		output.write('\n')
	print 'PREDICTION FILE GENERATED !!!!!!'


if __name__ == "__main__":
	readFile (dir)

# #############################Main Function#####################################################
# def main():
#     try:
#         arg1 = sys.argv[1]
#         arg2 = sys.argv[2]
#         print "Predicting the class unseen documents :: \n\n"
#         print "Prediction based on given model file ->", arg1
#         print "Unseen documents are present at location  ->", arg2
#         option = len(sys.argv)
#         if option == 3:
#             readFile(arg1,arg2)
#             print "Prediction Completed"
#         else:
#             if option == 2:
#                 print " Missing Prediction file name"
#                 exit(0)
#             else:
#                 print "Enter required filename. Try Again!!"
#                 exit(0)
#     except:
#         print "Some unwanted issue occurred!! Try once again"
#         exit(0)
#
# #######################Main Function#######################################
# if __name__ == "__main__":
#     main()