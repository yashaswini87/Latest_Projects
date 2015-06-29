import MapReduce
import sys
import json
from itertools import chain
mr = MapReduce.MapReduce()
"""
Inner join using Python MapReduce Framework
"""

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    #words = value.split()
    #for w in words:
    mr.emit_intermediate(value, key)

def reducer(key, c):
    
    script=open(sys.argv[1])
    
    for line in script:
        record=json.loads(line)	
     	if (key==record[1] and record[0]=='order'):
            s=[]
            s.append(record)
            s= list(chain(*s))
     	elif (key==record[1] and record[0]!='order'):
            t=[] 
            t.append(record)
            t=list(chain(*t))
	    k=s+t
            #somelist.append(s+t)	
   	    mr.emit(k)
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
