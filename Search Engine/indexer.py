__author__ = 'Sarita Joshi'
#########################Importing Python Libraries############################
from itertools import groupby
import sys
import re
regex = re.compile(r'^-?[0-9]+$')   #Reg Expression for filtering numeric index
########################Indexer################################################
###########List of linklist and Dictionary used in the Indexing  Program#######
#############################Data Dictionaries#################################
document = {}               #Document dictionary storing doc id and values
word_docid_freq =[]         #List that Stores word with doc id and tf details
line = []                   #List to read corpus text
index = {}                  # Dictionary storing inverted indexes
######################Reading File Content#####################################

def input_file_content(file):
    with open(file,"r") as f:
        input_data = f.read()       #Reading from given corpus file
    line = input_data.split()   #Lambda function for split based on '#'
    split_data = [list(group) for k, group in groupby(line,lambda x: x == '#') if not k]
    for e_lists in split_data:
        for each in e_lists:
            document[e_lists[0]] = e_lists[1:]
    for key,values in document.items():     #Filtering Numeric Index Values
        filtered_values = filter(lambda i: not regex.search(i), values)
        document[key] = filtered_values

###############################################################################
#######################Output file generated for Inverted Index################
################# index.out file generated#####################################
def redirect_output(output_file):
    i = 0
    file = open(output_file,"w")         #index.out file creation
    for key,values in index.items():
        file.write(str(key) + "\t")
        file.write(str(index[key]))
        file.write("\n")
    file.close()
#################Indexer Function####################################
def indexer(input_file,output_file):
    frequencies = {}                      #Initial Frequency as Null
    input_file_content(input_file)       #Reads corpus file content
    for key,each_lst in document.items():   #Iterate documents
        for each in each_lst:
            if each in frequencies:
                frequencies[each] += 1     # Already existing
            else:
                frequencies[each] = 1      # New occurrence
        for k,values in frequencies.items():  #intermediate list for index creation
            word_docid_freq.append((k,key,values))  #word_docid_frequency format
        frequencies = {}        # Initialize back to null

    for w,d,f in word_docid_freq:
        index.setdefault(w,[]).append((d,f,))
    print "No of words indexed (excludes numeric token)->",len(index)   #Print Index length
    redirect_output(output_file)     #Redirect the result to output file
####################Main Function##############################################
def main():
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        print " Indexer Implementation :: \n\n"
        print "Loads the given corpus file ->",arg1
        option=len(sys.argv)
        if option == 3:
            indexer(arg1,arg2)
            print "Indexing Completed"
        else:
            if option == 2:
                print " Missing Output file Details"
                exit(0)
            else:
                print "Enter required filename. Try Again!!"
                exit(0)
    except:
        print "Some unwanted issue occurred!! Try once again"
        exit(0)
#######################Main Function#######################################
if __name__ == "__main__":
	main()
##############################End of Inverted Index Creation###################
