import sys
import json

def hw(string):
    afinnfile = open(string)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
  	term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  	scores[term] = int(score)  # Convert the score to an integer.
    return list(scores.items()) # Print every (term, score) pair in the dictionary	
#print 'Hello, world!'


def main():
    s = hw(sys.argv[1])
    readfile=open(sys.argv[2])
    for line in readfile:
	sum1=0	
	try:
	       s1=json.loads(line)
	       k=s1["text"].encode('utf-8') 
	       sum1=lines(k, s)
               print sum1		
        except KeyError:
	       pass
   
		
    # here i need to read the second argument to parse using json libraries 
    

def lines(line, list1):
  # Reading a line in a file 
  # Tokenize and for each tokenized work check if the word is in the list
  # If the word is in the list increase the score by a value
    words=line.split()
    total=0  
    for word in words:
	word=word.lower()
	for item in list1:
	    if word==item[0]:
		total=total+item[1]
            else: 
		total=total+0   
    return total		
  
if __name__ == '__main__':
    main()
