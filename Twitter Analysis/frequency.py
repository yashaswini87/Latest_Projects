import sys
import json
from math import ceil
# Identifying the term frequency for the twitter file

def main():
    total_wordcount=[]
    tweet_file = open(sys.argv[1])
    for line in tweet_file:
        try:
	       s1=json.loads(line)
	       k=s1["text"].encode('utf-8') 
               words=k.split()
	       for word in words:
           	   total_wordcount.append(word)	
               
	except KeyError:
	       pass
    total_occurence= len(total_wordcount)
    
    for word in total_wordcount:
	frequency=0  		
        term_occurence=total_wordcount.count(word)
        frequency=ceil((float(term_occurence)/float(total_occurence))*10000)/10000.0
        print word, frequency
if __name__ == '__main__':
    main();
