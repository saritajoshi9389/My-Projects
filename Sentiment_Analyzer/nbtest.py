import operator

__author__ = 'Sharmodeep Sarkar and Sarita Joshi'
#########################Importing Python Libraries############################
import sys,os
from math import log
import pickle
import re
################################################################################
###########List of linklist and Dictionary used in the evaluation Program######
#############################Data Dictionaries#################################
PosTermProb = {} #holds the term and probability for data retrieved from model, Positive class
PosLen = 0		#Holds total positive word occurrences
NegTermProb = {}	 #holds the term and probability for data retrieved from model, Negative class
NegLen = 0		#Holds total negative word occurrences
Pp = 0					 # class prior label positive
Pn = 0 						# class prior  label negative
VocabLen =0				#Vocabulary length
PosFiles = []			#Stores list of all pos files predicted
NegFiles = []			#Stores list of all negative files predicted
UnpredictableFiles = []	#Stores list of unpredictable file if any
PredictTable = []			#Stores the filename storing the file, pos and neg scores
SortedPosProb = []			#Sorted Probability , Positive class
SortedNegProb = []			#Sorted Probability , Negative class
PosNegWeight = {}			#Stores the word Postive/Negative weight (log)
NegPosWeight = {}			#Stores the word Negative/Positive weight (log)

def readFile (testDir):
	global PosTermProb,NegTermProb,Pp,Pn,VocabLen,PosLen,NegLen,SortedNegProb,SortedPosProb
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
	print len(PosTermProb) , '  ', len(NegTermProb) , '  ' , Pp, Pn
	filenames = os.listdir( testDir ) # List of filenames in the test dir
	testDir+='\\'
	predictClass ([testDir + f for f in filenames])
	for key,value in dict(PosTermProb).items():
		PosNegWeight[key] = log(value) - log(NegTermProb.get(key,(1.0/(NegLen + VocabLen))))
	for key,value in dict(NegTermProb).items():
		NegPosWeight[key] = log(value) - log(PosTermProb.get(key,(1.0/(PosLen + VocabLen))))
	SortedPosProb = (sorted(PosNegWeight.items(), key=operator.itemgetter(1), reverse=True))[:20]
	SortedNegProb = (sorted(NegPosWeight.items(), key=operator.itemgetter(1), reverse=True))[:20]
	writeWordList()  #Prints the word list of 20

# Writes the word list of 20 terms
def writeWordList():
	global SortedNegProb,SortedPosProb
	with open('ListOfPosNeg.txt','w') as output:
		output.write("List 20 Terms with highest(log) ratio of Positive to Negative Weight \n\n")
		output.write('{:>10}\t\t{:>20}'.format("WORD","LOG RATIO") +"\n")
		i = 0
		while i < len(SortedPosProb):
			output.write('{:>10}\t\t{:>20}'.format(SortedPosProb[i][0],str(SortedPosProb[i][1]))+ "\n")
			i += 1
	output.close()
	with open('ListOfNegPos.txt','w') as output:
		output.write("List 20 Terms with highest(log) ratio of Negative to Positive Weight \n\n")
		output.write('{:>10}\t\t{:>20}'.format("WORD","LOG RATIO") +"\n")
		i = 0
		while i < len(SortedNegProb):
			output.write('{:>10}\t\t{:>20}'.format(SortedNegProb[i][0],str(SortedNegProb[i][1]))+ "\n")
			i += 1
	output.close()

##########################Predict Class###############################################################
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
		#input = re.sub(ur"[^\w\d'\s-]+",' ',input)
		input = input.replace('\n', ' ')
		words = input.split()
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

#####################################Calculate Pos Score
def getPosScore (lisOfWords):
	posScore = log(Pp)
	for word in lisOfWords:
		posScore += log(PosTermProb.get(word,(1.0/(PosLen + VocabLen))))
	return posScore


def getNegScore (lisOfWords):
	negScore = log(Pn)
	for word in lisOfWords:
		negScore += log(NegTermProb.get(word,(1.0/(NegLen + VocabLen))))  # to match Akshay's val replace NegLen by PosLen
	return negScore


############################Displays percentage calculation##############################
def calcPercentage(totalFiles,posFiles,negFiles):
	posFilePercentage = posFiles/(totalFiles*1.0)*100
	negFilePercentage = negFiles/(totalFiles*1.0)*100
	print 'totalFiles ', totalFiles
	print "Postive Files % = " , posFilePercentage
	print posFiles
	print "Negative Files % = ", negFilePercentage
	print negFiles

##############################Writes the output to text file
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


#############################Main Function#####################################################
# def main():
#     try:
# 		arg1 = sys.argv[1]
# 		arg2 = sys.argv[2]
# 		print "Predicting the class unseen documents :: \n\n"
# 		print "Prediction based on given model file ->", arg1
# 		print "Unseen documents are present at location  ->", arg2
# 		option = len(sys.argv)
# 		if option == 3:
# 			readFile(arg1,arg2)
# 			print "Prediction Completed"
# 		else:
# 			if option ==2:
# 				print "Missing Output file Name"
# 				exit(0)
# 			else:
# 				print " Missing File Directory name"
# 				exit(0)
#     except:
#         print "Some unwanted issue occurred!! Try once again"
#         exit(0)

#######################Main Function#######################################
if __name__ == "__main__":
    readFile(dir)