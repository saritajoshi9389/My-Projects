__author__ = 'Sharmodeep Sarkar and Sarita Joshi'
#########################Importing Python Libraries############################
import sys,os
from math import log
import pickle
import re
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

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

def readFile (testDir,n):
	global PosTermProb,NegTermProb,Pp,Pn,VocabLen,PosLen,NegLen
	print 'inside'
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
	predictClass ([testDir + f for f in filenames],n)


def predictClass (listOfFilenames,n):
	global PosFiles,NegFiles
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
		#words = input.split()
		# getting the list of bigrams 
		words = getBigrams(input,n)
		posScore = getPosScore(words)
		negScore = getNegScore(words)
		if (posScore>negScore):
			PosFiles.append(filename)
		if (posScore<negScore):
			NegFiles.append(filename)
		else:
			UnpredictableFiles.append(filename)
		print filename , " posScore  ", posScore, " negScore  ", negScore
	calcPercentage (len(listOfFilenames),len(PosFiles),len(NegFiles))    # TEST METHOD !!!!! CALCULATING % OF FILES IN EACH CLASS
	writePredictionFile ()


def getBigrams(text,n):
	token=nltk.word_tokenize(text)
	bigrams=ngrams(token,n)
	#compute frequency distribution for all the bigrams in the text
	fdist = nltk.FreqDist(bigrams)
	return fdist.keys()


def getPosScore (lisOfWords):
	posScore = log(Pp)
	for word in lisOfWords:
		posScore += log(PosTermProb.get(word,(1.0/(PosLen + VocabLen))))
	return posScore


def getNegScore (lisOfWords):
	negScore = log(Pn)
	for word in lisOfWords:
		negScore += log(NegTermProb.get(word,(1.0/(NegLen + VocabLen)))) 
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
	print ("Writing Prediction File ")
	output=open("prediction.txt",'w')
	output.write('Positive Files\n')
	for filename in PosFiles:
		output.write(filename)
		output.write ('\n')
	output.write('\n\n')
	output.write('Negative Files\n')
	for filename in NegFiles:
		output.write(filename)
		output.write('\n')
	print 'PREDICTION FILE GENERATED !!!!!!'


if __name__ == "__main__":
	readFile (dir,n)