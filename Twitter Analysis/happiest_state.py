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
    dic={}
    for line in readfile:
	sum1=0	
	try:
	   s1=json.loads(line)
           k=s1["place"]
           if k==None:
              pass
           else:
              if k["country"]=="United States":
                 t=k["full_name"][-2:]    
                 k1=s1["text"].encode('utf-8') 
                 sum1=lines(k1, s)
                 if t in dic.keys():
                    dic[t].append(sum1)
                 else:
                    dic[t] = [sum1]		
        except KeyError:
	   pass
    for key in dic.iterkeys():
    	dic[key] = sum(dic[key])
    inverse = [(value, key) for key, value in dic.items()]
    print max(inverse)[1]     		
    # here i need to read the second argument to parse using json libraries 
    

def lines(line, list1):
  # Reading a line in a file n
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
