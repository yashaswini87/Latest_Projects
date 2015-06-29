import pandas as pd
import os
from pandas import *
import numpy as np

# cleaning 2006 data
df2006=pd.read_csv('/home/yashu/Desktop/assignmentclasses/homework_04/2006.csv') # Change the path location
pd.set_printoptions(max_columns=841) # Optional: Testing to print all the columns. 
total_count=df2006.ix[:,0].count() # Counting total number of rows including missing
df2006=df2006.applymap(lambda x : np.nan if x == -999 else x) # applymap iterates through every cell in dataframe
required_col=[]# declare an empty list to store the required list
for col in df2006.columns:
    if float(float(df2006[col].count())/float(total_count))>=0.7: #the cut off is 30%, if the data has more than 30% missing the columns are chopped
        required_col.append(col)# Storing the required columns
df2006_processed=df2006[required_col]

# cleaning 2010 data
df2010=pd.read_csv('/home/yashu/Desktop/assignmentclasses/homework_04/2010.csv')
total_count_1=df2010.ix[:,0].count() # Counting total number of rows including missing
df2010=df2010.applymap(lambda x : np.nan if x == -999 else x) # applymap iterates through every cell in dataframe
required_col_1=[]# declare an empty list to store the required list
for col in df2010.columns:
    if float(float(df2010[col].count())/float(total_count_1))>=0.7: #the cut off is 30%, if the data has more than 30% missing the columns are chopped
       required_col_1.append(col)# Storing the required columns
df2010_processed=df2010[required_col_1]

#Reindexing the values
col1 = df2006_processed.columns.intersection(df2010_processed.columns)
df2006_clean = df2006_processed.reindex(columns=col1)
df2010_clean = df2010_processed.reindex(columns=col1)
