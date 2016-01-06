__author__ = 'sarita joshi'
################################Code for a Web Crawler - Both Unfocused and Focused Crawling for a given SEED and Keyphrase################################
###############Function built : Crawler(Seedurl,Keyphrase) , focused(seedurl,keyphrase) , unfocused(seedurl)##############################################
################### Datatype Used : 3 Link list that is seedlist , nexturls, visitedlist or paramlisturls#################################################
######################################### Importing Python Libraries ######################################################################################

import urlparse
import urllib
from bs4 import BeautifulSoup
import time
import re
import sys

##################################################End import ############################################################################################
##################################################List of variable and list used in the program#########################################################
seedurl = "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
seedlist = [seedurl]
visitedlist = []
nexturls = [seedurl]
paramlisturls = []

###############Start of main crawler Function that will call either focused or unfocussed crawling based on the Keyphrase###############################

def Crawler(seedurl,keyphrase):
    if keyphrase != "":
        keyphrasen = re.compile(keyphrase,re.IGNORECASE)
        display_urls = focused(seedurl,keyphrasen)
    else:
        display_urls = unfocused(seedurl)
################################Directing output to a text file#######################################################################################
    file = open("URLlist.txt","w")
    for i in display_urls:
        file.write(str(i))
        file.write("\n")
    file.close()
################################################End of main crawler function###############################################################################
################################################Start of Focused Crawler###################################################################################
def focused(seedurl,keyphrasen):
    nexturls = [seedurl]
    depth = 0
    flag = 0
    page = 0
    pagelimit = 0
    count = 0
    while depth < 5:
        depth += 1
        seedlist = []
        seedlist = nexturls[:]
        while len(nexturls) > 0: nexturls.pop()
        for url in seedlist:
            seedurl = url
            try:
                text = urllib.urlopen(seedurl).read()
                time.sleep(1)
                soup = BeautifulSoup(text,"html.parser")
            except:
                print " Some issue encountered.Trying again  \n"
                continue
            page += 1
            if page > 1002:
                print "Max 1000 URLs crawled. No of relevant URLs containing concordance as keyphrase is :", len(set(paramlisturls)), "Depth reached :",depth
                pagelimit = 1
                break
            soup1 = (soup.get_text()).encode('utf-8')
            if keyphrasen.search(soup1):
                if flag == 0 and url not in paramlisturls:
                    paramlisturls.append(seedurl)
                    count += 1
                    print "Page added",count
                    print "Added",seedurl
                    if len(paramlisturls) > 1000:
                        flag = 1
                        break
                    links = soup.findAll('a', href=True)
                    for linktag in links:
                        tag = linktag['href']
                        tag = urlparse.urljoin('https://en.wikipedia.org/wiki/', tag)
                        if tag.startswith('https://en.wikipedia.org/wiki') and '#' not in tag and not "Main_Page" in str(tag) and tag.count(':') <= 1 and tag not in nexturls and tag != "https://en.wikipedia.org/wiki/":
                            nexturls.append(tag)
            if flag == 1:
                break
        if pagelimit == 1:
            break
        print "Current Depth : ", depth, "and Number of relevant URLs till this depth is :", len(set(paramlisturls)), "No of pages crawled is",page
    return paramlisturls
######################################################End of Focused Crawling###############################################################################################
######################################################Start of Unfocused Crawling###########################################################################################
def unfocused(seedurl):
    nexturls = [seedurl]
    depth = 0
    flag = 0
    page = 0
    while depth <= 5:
        if flag == 1:
             break
        depth += 1
        seedlist = []
        seedlist = nexturls[:]
        while len(nexturls) > 0:
            nexturls.pop()
        for url in seedlist:
            seedurl = url
            try:
                text = urllib.urlopen(seedurl).read()
                time.sleep(1)
                soup = BeautifulSoup(text,"html.parser")
            except:
                print "Some issue encountered. Trying again"
                continue
            if seedurl not in visitedlist and flag == 0:
                visitedlist.append(seedurl)
                print "Added :", seedurl
            links = soup.findAll('a', href=True)
            for linktag in links:
                tag = linktag['href']
                tag = urlparse.urljoin('https://en.wikipedia.org/wiki/', tag)
                if tag.startswith('https://en.wikipedia.org/wiki/') and '#' not in tag and "Main_Page" not in str(tag) and tag.count(':') <= 1 and tag not in nexturls and tag != "https://en.wikipedia.org/wiki/":
                    nexturls.append(tag)
            if len(visitedlist) > 999:
                flag = 1
                break
        print "Depth for without keyphrase check: ", depth, "No of Urls at this level", len(visitedlist)
        if flag == 1:
            break
    return visitedlist
##########################################################End of UnFocused Crawling###############################################################################
#################################################Main Function####################################################################################################
def main():
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        print "The seedurl URL is  \n",arg1," The keyphrase if provided is  \n", arg2
        option = len(sys.argv)
        if option == 3:
            starttime = time.time()
            Crawler(arg1,arg2)
            endtime = time.time()
            print "\n\n Execution Time in seconds :",endtime - starttime
        else:
            if option == 2:
                starttime = time.time()
                Crawler(arg1,"")
                endtime = time.time()
                print "\n\n Execution Time in seconds : ",endtime - starttime
            else:
                print "Incorrect. Please try again"
                exit(0)
    except:
        print "Wrong input. Try again with correct seedurl and keyphrase"
        exit(0)
if __name__ == "__main__":
	main()
################################################## Main Ends ################################################################################################################