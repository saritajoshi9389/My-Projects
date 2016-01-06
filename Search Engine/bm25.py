__author__ = 'Sarita Joshi'
##########################Importing required python libraries##################
from math import log
import sys
import re
import operator
from itertools import izip
from collections import defaultdict
###################Data Structures#############################################
results = []        #List for storing the results for each given query
indexes = {}        #Dictionary that stores the calculated inverted index values
docids_length = {}  #Dictionary that stores the Doc Ids along with length of
                    # documents
#################Constants for BM25 Calculation################################
# We are implementing BM25 based on calculated Inverted Indexes for terms,
# ignoring any tokens that contain only the digits 0-9
###################Fixed Values to be used for calculating value of K#########
k1 = 1.2
b = 0.75
k2 = 100
SYSTEM_NAME = "SARITA_RUN"      #Default System Name for a run
#######No relevance Information is available###################################
R = 0.0
r = 0
###################BM25 Implementation#########################################
# This Function retrieves the given inverted Index file name "index.out",
# "queries.txt" that contains 7 queries and a maximum number of document
# result
def bm25_implementation(index_file, query_file, no_docs):
    try:
        file = open(index_file, "r")         # Retrieve Inverted Index
        itemization = iter(re.split('\t|\n', file.read()))
        dic = dict(izip(itemization, itemization))
        for k in dic.keys():
            if not dic[k]:
                del dic[k]
        for key, value in dic.items():
            tList = filter(None, re.split('[|(|\'|:|)|,| |]', value))
            i = 1
            while i < (len(tList) - 1):
                if key not in indexes.keys():
                    indexes[key] = {tList[i]: tList[i + 1]}
                else:
                    indexes[key].update({tList[i]: tList[i + 1]})
                i += 2
        file.close()
    except:
        print "File Can't be read", file
        exit()

##################Completed retrieval of Inverted Indexex######################
#################Calculation of Document lengths###############################
    for key,value in indexes.items():
        for item in value.items():
            if item[0] not in docids_length.keys():
                docids_length[item[0]] = int(item[1])
            else:
                docids_length[item[0]] += int(item[1])
    avdl = float(sum(docids_length.values()))/float(len(docids_length))

# avdl stores the average documents length that is length of all documents
# divided by total number of documents in the given corpus "tccorpus.txt"
####################Retrieve Input Query#######################################
# Code to retrieve queries from input argument "queries.txt"

    with open(query_file,"r") as file:
        file_input = file.read()
        query_list = filter(None, re.split(' \n', file_input))
    for queries in query_list:
        results.append(process_query(queries, avdl))
    display_ranking_output(results, no_docs)
    file.close()

# Calls the display_ranking_output that displays the ranking results for top 100
# 100 documents for each query

#################Display ranking Score############################################
# ************ Creates a results.eval file for storing the final run result *******

def display_ranking_output (results, no_docs):
    int_no_docs = int(no_docs)
    query_id = 1            # Query Id starts with 1
    for query_result in results:  #Sorting in decreasing rank of document
        sorted_list = sorted(query_result.iteritems(), key=operator.itemgetter(1), reverse=True)
        initial_rank = 1
        with open("results.eval", "a") as output_file:
            for i in sorted_list[:int_no_docs]:
                temp = (query_id, i[0], initial_rank, i[1], SYSTEM_NAME)
                output_file.write(str('{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\t{:>12}'.format(*temp)) + "\n")
                print '{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\t{:>12}'.format(*temp)
                initial_rank += 1
            query_id += 1
    output_file.close()

# ############################Processing Single Query###############################
# Function to calulate BM25 score BM25(Q,D) i.e for a given query it checks for all
# documents that have the query terms, from the input query

def process_query (query, avdl):
    query_output = dict()
    #qf = 1
    N = len(docids_length)
    q_dic = defaultdict(int)
    for word in query.split():
        q_dic[word] += 1
    for query_term in query.split():
        if query_term in indexes.keys():
            qf=q_dic[query_term]
            single_doc_dic = indexes[query_term]
            for doc_id, doc_freq in single_doc_dic.items():
                n = len(single_doc_dic)
                f = doc_freq
                dl = docids_length[doc_id]
                score = calculate_BM25_score(n,f,qf,r,N,dl,avdl) #Calculates BM25 score (Q,D)
                if doc_id in query_output:
                    query_output[doc_id] += score # Summation of BM25 scores
                else:
                    query_output[doc_id] = score  #New entry
    return query_output

######################Calculate Normalizing Factor##################################
# K is a more complicated parameter that normalizes the tf component by document
# length

def calculate_K_value(dl,avdl):
    return k1*((1-b) + (b*(float(dl)/float(avdl))))

####################################################################################
#########################calculating BM25 score#####################################
# n = no if docs containing the term
# f = frequency of a term in a particular document
# qf = query frequency of the term
# r = relevant documents containing the term
# R = relevance information
# dl = length of the document
# avdl = average length of the documents
# N = Total no of documents in the collection
#################################BM25 Calculation####################################
def calculate_BM25_score(n,f,qf,r,N,dl,avdl):
    K = calculate_K_value(dl,avdl)
    term1 = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    f = int(f)
    term2 = ((k1 + 1) * f) / (K + f)
    term3 = ((k2 + 1) * qf) / (k2 + qf)
    return term1 * term2 * term3
####################################################################################
########################Main Function###############################################
def main():
    try:
        with open("results.eval","w") as f:f.flush()
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        print "Start BM25 :: \n\n"
        print "Loads the Inverted Index file ::", arg1
        print "Loads the Query File ::", arg2
        print "Loads the maximum number of document result ::", arg3
        option = len(sys.argv)
        if option == 4:
            print "Algorithm in progress------->"
            bm25_implementation(arg1,arg2,int(arg3))
            print "BM25 Finished"
        else:
            if option == 3:
                print "Max Number of Docs to print not present"
                exit(0)
            else:
                if option == 2:
                    print "Query text file not present"
                    exit(0)
                else:
                    print "File name not entered"
                    exit(0)
    except:
        print "Error!! Try once again"
        exit(0)

##############################Main#############################################
if __name__ == "__main__":
    main()
#################End of BM25 Implementation####################################
