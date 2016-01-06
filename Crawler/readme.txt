******************************Web crawler : Setup, Compilation and Execution guidelines********************************************************************

This is a webcrawler code designed in python 2.7
For this code to be executed on any terminal , we need to have below pre-requisites met:

1)Python 2.7 installed
2)Python package beautiful soup installed

For step 1)
Goto https://www.python.org/downloads/ -> install as per operating system

For step 2)
Goto http://www.crummy.com/software/BeautifulSoup/ -> Download the latest version of beautiful soup i.e 4.4-> untar BeautifulSoup and place the bs4 library to python Lib folder (ex C:\Python27\Lib)
or same can be done using command

	python -m pip install BeautifulSoup

Place the webcrawler.py file to any particular location

Once the above pre-requisites are met, we can run this program as below.(Unfocused and Focused crawling)

1)Go to terminal
2)Type python. This will start the python shell terminal
3)Go to the required path and run py file as below
FilePath/WebCrawler.py "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher" "concordance" (This is for two inputs that is seedurl and keyphrase)
					OR
FilePath/WebCrawler.py "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher" ""             (This is only with seedurl. Blank string to be provided in the absense of keyphrase )
4) URLs retrieved after crawling as per given problem statement will be displayed at the terminal and also a URLlist.txt file will be created at the python base location.

For unfocused crawling without keyphrase, estimated time taken to get the result is 1500 to 1600 seconds (based on time at which the program is executed and a delay of atleast 1 second between requests to web server- Politeness Factor)

For focused crawling with keyphase as 'Concordance', estimated time taken is 1400-1500 seconds (based on time at which the program is executed and a delay of atleast 1 second between requests to web server - Politeness Factor)

**************************************Observations :(for 1000 unique crawling)**********************************************************************

1) The proportion of number of pages retrieved by focused crawler 'Concordance'(n) to the number of pages crawled(N) : n/N = 56/1000 = 0.056 (5.6%). 
Estimated time taken with atleast a delay of 1sec(Politeness Factor): 1400 to 1500 secs 

2) Estimated time taken to run the unfocused crawling resulting in 1000 unique URLs : 1500 to 1600 secs

Note : This result varies a lot based on bandwidth, Network glitches.
****************************************************References**************************************************************************************
1) http://www.tutorialspoint.com/
2)https://www.youtube.com/
3)http://www.crummy.com/software/BeautifulSoup
***************************************************** NOTE******************************************************************************************
NOTE: The proportion of number of pages retrieved  by focused crawler 'Concordance'(n) to the number of pages crawled(N) : 258/18000 for focussed crawling. Time taken with alteast a delay of 1 sec (politeness factor) : 2 hours 36 mins (Scenario when the crawler continues untill depth 5 is crawled)
Major issue encoutered : the Connectivity reset by peer issues / Gateway connection closed.
