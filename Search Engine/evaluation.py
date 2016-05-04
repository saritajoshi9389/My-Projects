__author__ = 'Sarita Joshi'
#########################Importing Python Libraries############################
from string import lstrip
from collections import OrderedDict
import sys
import re
import math
########################Evaluation################################################
###########List of linklist and Dictionary used in the evaluation Program######
#############################Data Dictionaries#################################
evalLst = {}  # Document dictionary storing the HW4 lucene output
sorted_evalList = {}    # Document dictionary storing the HW4 lucene output,sorted by key i.e. Query Id
stdLst = {}  # Document dictionary storing relevance judgement for test CACM
table = []  # List that stores the required calculation querywise in a format
new_table = []  # List storing the above calculations along with NDCG values
##############################################################################
# file1 is the result from the LUCENE based search engine
# file2 is the CACM standard result file
def fileReader(file1, file2):
    ##############This code reads the arg1 as the result from lucene#########
    try:
        print ("Reading HW4 lucene output for three queries")
        with open(file1,"r") as file:
            input = file.read()
            line = input.split('\n')    #split based on new line
    except:
        print "Given input File Can't be read", file
        exit()
    for each_line in line:
        each_line = re.sub("Q0|SARITA", "", each_line)
        if each_line[0] not in evalLst.keys():
            evalLst[each_line[0]] = [each_line[2:].strip()]    # A new entry
        else:
            evalLst[each_line[0]].append(each_line[2:].strip())    #Already existing, just append
    ###############This code reads the relevance judgement, arg2 ############
    try:
        print ("Reading the relevance judgement file for test CACM\n")
        with open(file2,"r") as f:
            input = f.read()
            line = input.split('\n')       #split based on new line
            line = line[:len(line) - 1]
    except:
        print "Error reading the relevance judgement file", f
        exit()
    ### Below code checked for document number id, changes query ids as below
    ### Query id '12' -> '1' || portable operating systems
    ### Query id '13' -> '2' || code optimization for space efficiency
    ### Query id '19' -> '3' || parallel algorithms
    for each_line in line:
        splitList = each_line.split()
        splitList[2] = re.sub('CACM-', '', splitList[2])
        if splitList[0] in ('12', '13', '19'):
            if splitList[0] == '12': changedId = '1'
            if splitList[0] == '13': changedId = '2'
            if splitList[0] == '19': changedId = '3'
            if changedId not in stdLst.keys():
                stdLst[changedId] = [splitList[2]]
            else:
                stdLst[changedId].append(splitList[2])
    sorted_evalList = OrderedDict(sorted(evalLst.items(), key=lambda x: x[0])) #Sorts the evaluation result dict on key
    calculate_recall_precision(sorted_evalList)         # Function that does the entire calculation
################### End of required file reading############################################
#           Recall is number of retrieved relevant documents/ Total relevant documents
#           Precision is number of retrieved relevant documents/ Total retrieved documents till that point
#           Formula for DCG , Discounted Cumulative gain is
#           = rel1 + summation (i=2 to p) reli/logi to the base log2
#           Normalized DCG is DCG/IDCG for a particular rank p
#################### calc_recall_precision() function#######################################
def calculate_recall_precision(sorted_evalList):
    summed_AP = 0              # this holds the summmation of AP to be used for MAP
    for key, values in sorted_evalList.items():    # Outer loop for each query
        print "For Query ->", key
        tot_rel_doc = len(stdLst[key])     # Total number of relevant docs for a query with query id as key
        rel_ret_till_now = 0                # Counts the number of retrieved relevant document till now
        count_AP = 0                        # Count of number of precisions added up for MAP
        total_AP = 0                        # Total precision values calculated for MAP calculation for 3 queries
        temp_list = []                      # List that stores the Rank, relevance level for 100 docs for each query
        ndcg = []                           # Stores the NDCG values for each query i.e 100 documents for each query
        dcg = []                            # Stores the rank, relevance level, calculated DCG values for 100 docs of each query
        idcg = []                           # Stores the rank, relevance level, calculated IDCG values based on the relevance judgement
        idcg_list = []                      # Stores the rank, relevance level based on the relevance judgement data
        for doc in values:                  #Inner loop for ach document for that query key
            R = 0                           # Initialize relevance level variable R (R=0 -> Relevant, R=1 -> Non-Relevant)
            splitEvalLst = doc.split()     # Splitting the doc values and removing prefic "0", if any
            splitEvalLst[0] = lstrip(splitEvalLst[0], '0')
            if splitEvalLst[0] in (stdLst[key]):
                R = 1                       #If document is in the relevance judgement file, set R=1
                rel_ret_till_now += 1       # retrieved relevant files till now will be incremented by 1
            recall = rel_ret_till_now / (tot_rel_doc * 1.0)     #Formula for recall
            precision = (rel_ret_till_now * 1.0) / int(splitEvalLst[1])    #Formula for Precision
            ###########Average Precision calculation #############################################
            if R == 1:                      #If relevant file, add the precision for that document
                total_AP += precision
            count_AP = len(stdLst[key])    #Total relevant file
            temp_list.append([int(splitEvalLst[1]), R])         #Stores the rank and relevance level
            data_format = (splitEvalLst[1], splitEvalLst[0], splitEvalLst[2], str(R), precision, recall) #Output
            if splitEvalLst[1] == "20":    #Prints the Precision value for a query at Rank 20
                print "Precision at rank 20 for this query i.e. P@20 is ->", precision,"\n"
            formatted_content = '{:>2}\t{:>2}\t{:>2}\t{:>2}\t{:>20}\t{:>15}'.format(*data_format)
            table.append(formatted_content)      # table storing the output as per above format
        i = 2       #Counter variables to calculate DCG from rank 2
        j = 2       #Counter variables to calculate IDCG from rank 2
        print "Calculating the DCG values :"
        dcg_val = temp_list[0][1]
        dcg.append([temp_list[0], dcg_val])
        ###################Calculate DCG using formula################################################
        while i <= len(temp_list):
            dcg_val += (temp_list[i - 1][1]) / math.log(i, 2)
            dcg.append([temp_list[i - 1], dcg_val])
            i += 1
        count = 1
        #print "Total number of relevant documents for this query", len(stdList[key])
        ################################IDCG Calculation#############################################
        ##############Ranking the relevance judgement data based on relevance level##################
        for rank in range(1, 101):
            if count <= len(stdLst[key]):
                idcg_list.append([rank, 1])
            else:
                idcg_list.append([rank, 0])
            count += 1
        idcg_val = idcg_list[0][1]
        idcg.append([idcg_list[0], idcg_val])
        rank = 1
        while j <= len(idcg_list):                                      # IDCG calculation#
            idcg_list[rank][0] = j
            idcg_val += (idcg_list[j - 1][1]) / math.log(j, 2)          #Formula for IDCG calculation
            idcg.append([idcg_list[j - 1], idcg_val])
            j += 1
            rank += 1
        rank = 1
        while rank <= len(temp_list):                                   #Calulation of Normalized DCG
            ndcg.append(dcg[rank - 1][1] / idcg[rank - 1][1] * 1.0)
            rank += 1
        i = 0
        while i < len(ndcg):                                            #Append the calulated NDCG result to output
            new_table.append((table[i], str(ndcg[i])))
            i += 1
        AP = total_AP / count_AP                #Calculating Average precision for the query
        print count_AP, "are the total relevant documents for this query"
        print 'Average Precision for Query ', key, ' is ', AP        # key is the query_id
        fileWriter(key)                                              # Displaying querywise output
        summed_AP += AP                                         # AP accumulated till now
    ###################Mean Average Precision Calculation#################################################
    MAP = summed_AP / len(sorted_evalList)                             # Total accumulated AP/ 3 i.e total no. of queries
    print '\n', 'Mean Average Precision calculated  for these 3 queries is (MAP) = ', MAP
######################## Function to display querywise output############################################
# Displays 'RANK', 'DOC_ID', 'DOC_SCORE', 'RELEVANCE_LEVEL', 'PRECISION', 'RECALL', 'NDCG' for 100
# documents for each query
def fileWriter(query_id):
    output = open("table_" + query_id + ".txt", 'w')
    if query_id == '1':
        query = 'portable operating systems'
    if query_id == '2':
        query = 'code optimization for space efficiency'
    if query_id == '3':
        query = 'parallel algorithms'
    output.write('Table for Query -> ' + query + '\n\n')
    table_header = ('RANK', 'DOC_ID', 'DOC_SCORE', 'RELEVANCE_LEVEL', 'PRECISION', 'RECALL', 'NDCG')
    format_header = '{:>2}\t{:>2}\t{:>2}\t{:<8}\t{:>15}\t{:>15}\t{:>15}'.format(*table_header)
    output.write(format_header + '\n')
    global table
    global new_table
    i = 0
    while i < len(new_table):
        output.write(new_table[i][0] + '\t\t' + new_table[i][1] + '\n')
        i += 1
    new_table = []
    table = []
    output.close()
    print ("Data saved for query " + query_id +"\n")
########################End of file writer function############################################
#############################Main Function#####################################################
def main():
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        print " Evaluating Retrieval Effectiveness :: \n\n"
        print "Loads the result obtained in HW4 using lucene ->", arg1
        print "Loads the relevance judgement for CACM test collection ->", arg2
        option = len(sys.argv)
        if option == 3:
            fileReader(arg1,arg2)
            print "Evaluation Completed"
        else:
            if option == 2:
                print " Missing cacm.rel file Details"
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
##############################End of Result evalutaion###################

