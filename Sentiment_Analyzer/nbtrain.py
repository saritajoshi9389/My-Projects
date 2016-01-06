__author__ = 'Sharmodeep Sarkar and Sarita Joshi'
#########################Importing Python Libraries############################
import sys, os
import re
import pickle  # moved to pickle 'coz JSON can't handle decimal
from decimal import Decimal  # this gives more precision as compared to float
########################Trainer################################################
###########List of linklist and Dictionary used in the training Program######
#############################Data Dictionaries#################################
subDirList = []         # Stores OS directory
ontology = ['pos', 'neg']       # Ontology for pos and neg class
Pp = 0  # class prior label positive
Pn = 0  # class prior  label negative
V = []  # complete  Vocab of the entire corpus
NegTermFreq = {}  # holds all terms (in the docs )classified as neg with their frequency of occurance in all docs classified as neg
PosTermFreq = {}  # holds all terms (in the docs )classified as pos with their frequency of occurance in all docs classified as pos
PosTermProb = {}    #Holds terms along with calculated probability for positive class
NegTermProb = {}    #Holds terms along with calculated probablity for negative class
PosLen = 0          #Holds total word occurrence in positive class
NegLen = 0          #Holds Total word occurrence in negative class
VocabLen = 0        #Vocabulary length
modelFileContent = []       #Model file to be dumped

###################################3To retrieve OS directory structure##############
def getSubDir(dir):
    global subDirList
    for x in os.walk(dir):
        subDirList.append(x[0])
    del subDirList[0]
    calcClassPrior_TermFreq_Vocab()

#########################Calculates P(neg) and P(pos)#################################
def calcClassPrior_TermFreq_Vocab():
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
            createTermFreq([folder + f for f in filenames], 'neg')
        # Calculating instances in taining data with Negative label
        if ('pos' in folder):
            # Calculating instances in taining data with Positive label
            Np = len(filenames)
            # Making TermFreq for pos class and also buliding the Corpus Vocab
            # the folder name is prefixed to each of the file in the listofFileNames (filenames)
            createTermFreq([folder + f for f in filenames], 'pos')

    global Pp, Pn, modelFileContent
    Pp = Np / (N * 1.0)  # Class prior for label Positive
    # Class prior for label Negative
    Pn = Nn / (N * 1.0)
    print "Calculated Class Prior for Negative and Positive class ->",Pn, '', Pp
    createCorpusVocab()
    createTermProbability()
    modelFileContent = [PosTermProb,PosLen, NegTermProb,NegLen, Pp, Pn, VocabLen]
    #print modelFileContent
    with open("model.txt", 'w') as outfile:
        pickle.dump(modelFileContent, outfile)
    outfile.close()
    print 'Model File Ready !!!!!!'
    # Starting Stats Printing
    #print V
    print 'Generated Vocabulary Length ->' , VocabLen
    print 'Total Positive term Occurrences -> ',PosLen
    print 'Total Negative term Occurrences -> ',NegLen
    # End of Stats Printing

###############################Calculating term frequency as per class,split tokens#########################
def createTermFreq(listOfFilenames, cls):
    for filename in listOfFilenames:
        try:
            f = open(filename, 'r')
        except:
            print "File Can't be read", f
            exit()
        input = f.read()
        f.close()
        # Removing punctuations from inputs (hyphens are retained)
        #input = re.sub(ur"[^\w\d'\s-]+",' ',input)
        input = input.replace('\n', ' ')
        words = input.split()
        # updating the TermFreq Dic for the class to which this file belongs
        TermFreq(words, cls)
    # Adding the words in this list to the Corpus Vocab
    # updateCorpusVocab (words)

#############################Calculate the term frequency-main function##########################################
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

# checks whether the word count of the argument is greater than the threshold value############################
def isLegalTermCount (word):
    return PosTermFreq.get(word,0) + NegTermFreq.get(word,0)>=5

#######################Creates the Vocabulary corpus#########################################################
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
#############################################################################################################
#############################Calculate Term Probability######################################################
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


#############################Main Function#################################################################
# def main():
#     try:
#         arg1 = sys.argv[1]
#         arg2 = sys.argv[2]
#         print " Classifier -> Training the system :: \n\n"
#         print "Loads the file from train directory ->", arg1
#         print "Generates the model file name as  ->", arg2
#         option = len(sys.argv)
#         if option == 3:
#             getSubDir(arg1,arg2)
#             print "Training Completed"
#         else:
#             if option == 2:
#                 print " Missing Output Model file name"
#                 exit(0)
#             else:
#                 print "Enter required filename. Try Again!!"
#                 exit(0)
#     except:
#         print "Some unwanted issue occurred!! Try once again"
#         exit(0)

#######################Main Function#######################################
if __name__ == "__main__":
    getSubDir(dir)
