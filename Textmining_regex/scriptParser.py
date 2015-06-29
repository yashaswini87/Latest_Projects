#!/usr/bin/env python
from optparse import OptionParser
from collections import Counter
import sys
import re
import pdb


import homework_05_soln.src.common as common


def main():
    """
    reads a movie script text file and extracts data
    Examples
    ---------
    """
    usage = "usage: %prog [options] dataset"
    usage += '\n'+main.__doc__
    parser = OptionParser(usage=usage)

    parser.add_option(
        "-o", "--outfilename",
        help="Write to this file rather than stdout.  [default: %default]",
        action="store", dest='outfilename', default=None)

   # pdb.set_trace()
    (options, args) = parser.parse_args()

    ### Parse args
    # Raise an exception if the length of args is greater than 1
    assert len(args) <= 1
    # If an argument is given, then it is the 'infilename'
    # If no arguments are given, set infilename equal to None
    infilename = args[0] if args else None

      ## Get the infile/outfile
    infile, outfile = common.get_inout_files(infilename, options.outfilename)

    ## Call the function that does the real work
    organize(infile, outfile)

    ## Close the files iff not stdin, stdout
    common.close_files(infile, outfile)


def organize(infile, outfile):
    '''
    This is going to run all the parsing functions, organize the output and dump to outfile or stdout
    '''

    ###get the script
    script = infile.readlines()
    
    characters = getSpeakers(script)
    scenes = getScenesData(script)
   
    scriptData = {'Characters': characters, 'SceneData': scenes}
   
    outfile.write(str(scriptData))
   





       

###############################PARSING FUNCTIONS###################
def getSpeakers(script):
    '''
    This function will return the characters in a script. 

    Parameters
    ----------

    script: a list of lines in the script text file


    Returns
    -------

    speakers: list

    Note:
    -----
    There are a number of different ways to extract the speakers names from a script. One way is to first identify the position where these names appear, i.e. count the number of whitespace, and then extract just the name from the line. Since we are dealing with speakers and not with all characters, you can assume that each speaker is followed by a section of dialogue. You will also have to make sure that you are treating both whitespaces and tabs in the same manner; one way to do this is to convert all whitespaces to tabs with the re.sub(). 
    In order to minimize the number of false positives, we will only list speakers who appear more than once in the script. The Counter() funtion from the python collections library is a good choice for this. 
    '''
# declaring empty lists
    count_whitespace=[]
    s=[]
    speakers_list=[]
    words=[]
# Getting the count of whitespace before first character before a line
    for line in script:
	count_whitespace.append(getFirstNonSpacePos(line))
    while None in count_whitespace:
        count_whitespace.remove(None) 
# getting unique list of whitespace 
    k=list(set(count_whitespace))
# finding a,d which corresponds to the first maximum and forth maximum whitespace count
    a=sorted(k)[-1]
    d=sorted(k)[-5]
#for line in script:
    for line in script:
        if (d<=getFirstNonSpacePos(line) and getFirstNonSpacePos(line)<=a and script.count(line)>1):
           speakers_list.append(getSpeaker(line))
## for word in speakers_list keeping words which has punctuations and lowercases
    for w in speakers_list:
        match=re.search(r'[.?!,":\\;!()]',w)
    	if  match or w.islower()==True:
            words.append(w) 
## excluding words list from speakers_list
    return list(x for x in set(speakers_list) if x not in words)



def getFirstNonSpacePos(line):
    
    '''
    This funciton takes a line of text and returns the number of whitespace before the first non-whitespace character. If the line contains only whitespace it returns None.

    Parameters
    __________

    line: string

    Returns
    _______
    numeric or None
    
    '''
    count=0
    line1=re.sub('^\s+','\t',line) ##Replacing the white spaces with tabs
    if line1.strip()=='':
       count=0
    else:	
       k=line1.strip()[0][0]## extracting the first letter after tabs 	
       for i in line:
	   if i!=k:
	      count+=1
           else:
              break
    if count==0: 
	return None
    else:
    	return count	
    
def getSpeaker(line):
    '''
    This function extracts the speaker from the line. You will need to strip away everything but the speakers name, or title. 

    Parameters
    ----------

    line: string

    Returns
    -------
    string

    '''
    return line.strip()



def getScenesData(script):
    '''
    This function runs through the script and looks for line that have a scene marker ("INT/EXT" or such). It keeps track of the lines the scene starts and end, the type of scene it is (interior or exterior), and any additional description (such as location, directions, etc). The function returns a list containg the scene start/end lines, the type and descriptions. 

    Parameters
    ----------
    script: list of strings

    Returns
    -------
    list
    '''
    indexes = []
    descs = []
    whole = []
    scenes = []

    for num, line in enumerate(script):
        ###I used or in || format as I got errors that it does not recognize the condition so I separated the conditions
        if (sceneType(line) == 'INT'): 
            indexes.append(num)
            descs.append(getSceneDescription(line))
            scenes.append(sceneType(line))
        elif(sceneType(line) == 'EXT'):
            indexes.append(num)
            descs.append(getSceneDescription(line))
            scenes.append(sceneType(line))
    
    end = len(script)-1
    for count, desc in enumerate(descs):
        if(count+1 != len(descs)):
            whole.append((indexes[count], indexes[count+1], scenes[count], desc))
        elif(count+1 == len(descs)):
            whole.append((indexes[count], end, scenes[count], desc))
            
    return whole




def sceneType(line):
    '''
    Retrives the scene type. 

    Parameters
    ----------
    string

    Returns
    -------
    string: either "INT" or "EXT" depending on scene type

    '''
    line_temp = line
    match1 = re.search(r"INT.", line_temp)
    match2 = re.search(r"EXT.", line_temp)
    if(match1):
        if match1.group(0) == 'INT.':
            return "INT"
    elif(match2):
        if(match2.group(0) == "EXT."):
            return "EXT"
        


def getSceneDescription(line):
    '''
    This function retrieves the description of a scene. It takes a line that starts with a scene marker, such as INT or EXT, and retirves all the descriptive text 
    which follows the marker. Note, it also strips the text of surrounding whitespaces (recommend using the .strip() method in the string library). 

    Parameters
    ----------
    string

    Returns
    -------
    string

    '''
    skipped = line
    skipped = re.split('\d*', line)[-1]
    skips = getFirstNonSpacePos(skipped)
    if(type(skips) == int):
        if(sceneType(line) == 'INT'):
            line_temp = re.split('\s{%d}%s.\s'%(skips,sceneType(skipped)),skipped)[-1]
            return line_temp
        elif(sceneType(line) == 'EXT'):
            line_temp = re.split('\s{%d}%s.\s'%(skips, sceneType(skipped)),skipped)[-1]
            return line_temp

if __name__ == "__main__":
    main()

