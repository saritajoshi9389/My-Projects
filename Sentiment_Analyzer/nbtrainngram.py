__author__ = 'Sharmodeep Sarkar and Sarita Joshi'
#########################Importing Python Libraries############################
import sys, os
import re
import pickle  # moved to pickle 'coz JSON can't handle decimal
from decimal import Decimal  # this gives more precision as compared to float
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

subDirList = []
ontology = ['pos', 'neg']
Pp = 0  # class prior label positive
Pn = 0  # class prior  label negative
V = []  # complete  Vocab of the entire corpus
NegTermFreq = {}  # holds all terms (in the docs )classified as neg with their frequency of occurance in all docs classified as neg
PosTermFreq = {}  # holds all terms (in the docs )classified as pos with their frequency of occurance in all docs classified as pos
PosTermProb = {}
NegTermProb = {}
PosLen = 0
NegLen = 0
VocabLen = 0
modelFileContent = []
bigram_dic ={} 


def getSubDir(dir,ngrams):
    print ngrams
    global subDirList
    for x in os.walk(dir):
        subDirList.append(x[0])
    del subDirList[0]
    calcClassPrior_TermFreq_Vocab(ngrams)

# Calculates P(neg) and P(pos)
def calcClassPrior_TermFreq_Vocab(ngrams):
    N = 0
    Np = Nn = 0
    for folder in subDirList:
        folder += '/'  # Making the directory name so that files can be read from this path
        filenames = os.listdir(folder)  # List of filenames in the directory
        # calculating N
        N += len(filenames)
        if ('neg' in folder):
            # Calculating instances in taining data with Negative label
            Nn = len(filenames)
            # Making TermFreq for neg class and also buliding the Corpus Vocab
            # the folder name is prefixed to each of the file in the listofFileNames (filenames)
            createTermFreq([folder + f for f in filenames], 'neg',ngrams)
        # Calculating instances in taining data with Negative label
        if ('pos' in folder):
            # Calculating instances in taining data with Positive label
            Np = len(filenames)
            # Making TermFreq for pos class and also buliding the Corpus Vocab
            # the folder name is prefixed to each of the file in the listofFileNames (filenames)
            createTermFreq([folder + f for f in filenames], 'pos',ngrams)

    global Pp, Pn, modelFileContent
    Pp = Np / (N * 1.0)  # Class prior for label Positive
    # Class prior for label Negative
    Pn = Nn / (N * 1.0)
    print Pn, '', Pp
    createCorpusVocab()
    createTermProbability()
    modelFileContent = [PosTermProb,PosLen, NegTermProb,NegLen, Pp, Pn, VocabLen]
    #print modelFileContent
    with open('model-file', 'w') as outfile:
        pickle.dump(modelFileContent, outfile)
    outfile.close()
    print 'Model File Ready !!!!!!'
    # Starting Stats Printing
    #print V
    print 'VocabLen ' , VocabLen
    print 'PosTermProb length ' , len(PosTermProb)
    print 'NegTermProb length  ' , len(NegTermProb)
    f = open ('posFreq.txt','a')
    f.write (str(PosTermFreq))
    f.close()
    f = open ('negFreq.txt','a')
    f.write (str(NegTermFreq))
    f.close()
    print 'Total PosLen ',PosLen
    print 'Total NegLen ',NegLen
    # End of Stats Printing


def createTermFreq(listOfFilenames, cls,ngrams):
    print 'inside makeVocab_TermFreq'
    # print listOfFilenames
    for filename in listOfFilenames:
        print filename
        try:
            f = open(filename, 'r')
        except:
            print "File Can't be read", f
            exit()
        input = f.read()
        f.close()
        # Removing punctuations from inputs (hyphens are retained)
        input = re.sub(ur"[^\w\d'\s-]+",' ',input)
        input = input.replace('\n', ' ')
        #words = input.split()
        # updating the TermFreq Dic for the class to which this file belongs
        bigramFreq(input, cls,ngrams)
        #TermFreq(words, cls)
    # Adding the words in this list to the Corpus Vocab
    # updateCorpusVocab (words)


def bigramFreq(text, cls,n):
    token=nltk.word_tokenize(text)
    bigrams=ngrams(token,n)
    #compute frequency distribution for all the bigrams in the text
    fdist = nltk.FreqDist(bigrams)
    if (cls == 'pos'):
        for k,v in fdist.items():
            PosTermFreq[k] = PosTermFreq.get(k,0)+v
    if (cls == 'neg'):
        for k,v in fdist.items():
            NegTermFreq[k] = NegTermFreq.get(k,0)+v



'''
def TermFreq(text, cls):
    global NegTermFreq, PosTermFreq
    if (cls == 'pos'):
        for word in text:
            PosTermFreq[word] = PosTermFreq.get(word,0) + 1
            # print NegTermFreq
    if (cls == 'neg'):
        for word in text:
            NegTermFreq[word] = NegTermFreq.get(word,0) + 1
            # print PosTermFreq

'''

# checks whether the word count of the argument is greater than the threshold value
def isLegalTermCount (word):
    return PosTermFreq.get(word,0) + NegTermFreq.get(word,0)>=1


def createCorpusVocab():
    global V, VocabLen, PosLen, NegLen  # updating the Corpus Vocab List
    print 'Creating Corpus Vocab'
    for key, values in PosTermFreq.items():
        if isLegalTermCount(key) :
            V.append(key)
            PosLen += PosTermFreq[key]
    for key, values in NegTermFreq.items():
        if isLegalTermCount(key) :
            V.append(key)
            NegLen += NegTermFreq[key]
    V = set(V)
    VocabLen = len(V)


def createTermProbability():
    #term_count, term_count1 = 0
    print 'Calculating Probability'
    global PosTermProb, NegTermProb
    for key, values in PosTermFreq.items():
        if isLegalTermCount(key) :
            TempProb = Decimal((PosTermFreq[key] + 1.0) / (PosLen + VocabLen))
            PosTermProb[key] = TempProb
    for key, values in NegTermFreq.items():
        if isLegalTermCount(key) :
            TempProb = Decimal((NegTermFreq[key] + 1.0) / (NegLen + VocabLen))
            NegTermProb[key] = TempProb


if __name__ == "__main__":
    getSubDir(dir,int(ngrams))
