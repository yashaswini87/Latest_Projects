import sys
import json
from collections import Counter
def main():
    readfile=open(sys.argv[1])
    words=[]
    for line in readfile:
	    try:
	       s1=json.loads(line)
	       k=s1["entities"]["hashtags"]
	       if k==[]:
		  pass
	       else:
		  for dictionary in k:
		      if dictionary["text"]:
		         words.append(dictionary["text"])   
		         
	    except KeyError:
	       pass
    cnt = Counter(words)
    l=cnt.items()
    l.sort(key = lambda item: item[1])
    for item in l[-10:]:
	print item[0],float(item[1])
  
if __name__ == '__main__':
     main()
