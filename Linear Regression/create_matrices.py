from __future__ import division
import pandas as pd
import os
from pandas import *
import numpy as np
import statsmodels.iolib.foreign as smio
import matplotlib.pyplot as plt
pd.set_option('max_columns', 50)
pd.set_option('max_rows', 1000)

# get data and clean -- this is the work of Bonnie, Yash, and Eric
df2006= pd.read_csv('../data/processed/2006.csv')
pd.set_printoptions(max_columns=841) # Optional: Testing to print all the columns. 
total_count=df2006.ix[:,0].count() # Counting total number of rows including missing
df2006=df2006.applymap(lambda x : np.nan if x == -999 else x) # applymap iterates through every cell in dataframe
required_col=[]# declare an empty list to store the required list
for col in df2006.columns:
    if float(float(df2006[col].count())/float(total_count))>=0.7: #the cut off is 30%, if the data has more than 30% missing the columns are chopped
        required_col.append(col)# Storing the required columns
df2006_processed=df2006[required_col]
df2010= pd.read_csv('../data/processed/2010.csv')
total_count_1=df2010.ix[:,0].count() # Counting total number of rows including missing
df2010=df2010.applymap(lambda x : np.nan if x == -999 else x) # applymap iterates through every cell in dataframe
required_col_1=[]# declare an empty list to store the required list
for col in df2010.columns:
    if float(float(df2010[col].count())/float(total_count_1))>=0.7: #the cut off is 30%, if the data has more than 30% missing the columns are chopped
       required_col_1.append(col)# Storing the required columns
df2010_processed=df2010[required_col_1]
col1 = df2006_processed.columns.intersection(df2010_processed.columns)
df2006_clean = df2006_processed.reindex(columns=col1)
df2010_clean = df2010_processed.reindex(columns=col1)


# set a mask for determining which columns we'll use and how
# -1 = prediction variable
# 0 = drop
# 1 = keep
# 2 = factorize (we'll keep a dict with the possible values)
# 3 = only in the enhanced model
mask = np.zeros(len(df2006_clean.columns))
N = df2006_clean.shape[0]
for i in xrange(len(mask)):
    mask[23] = -1
    if i in [6,9,10,11,12,13,14,16,21,28,34,43,45,59]:
        mask[i] = 1
    elif i in [2,8,24,25]:
        mask[i] = 2
    elif i in [3,4,15,44]:
        mask[i] = 3

# for factorize variables, what are the allowed values other than 'no answer'?
# we'll leave 'no answer's blank for now and later fill them in with frequency weights
factor_vars = {'wrkstat': [1,2,3,4,5,6,7,8], 'marital': [1,2,3,4,5], 'region': [1,2,3,4,5,6,7,8,9], 'xnorcsiz': [1,2,3,4,5,6,7,8,9,10]}
factor_vars_lookup = {}

# for each factor variable, figure out the frequency weights
factor_weights = {}
factor_counts = {}
for var in factor_vars:
    factor_weights[var] = {}
    factor_counts[var] = {}
    for t in factor_vars[var]:
        factor_counts[var][t] = 0.
for i in xrange(df2006_clean.shape[0]):
    for var in factor_vars:
        t = df2006_clean.ix[i,var]
        if t in factor_vars[var]:
            factor_counts[var][t] += 1
for var in factor_vars:
    m = 0.
    for t in factor_counts[var]:
        m += factor_counts[var][t]
    for t in factor_counts[var]:
        factor_weights[var][t] = factor_counts[var][t] / m
        
K = 1 # start with 1 for a constant term
new_variable_names = []
for i in xrange(len(mask)):
    if mask[i] == 1:
        new_variable_names.append(df2006_clean.columns[i])
        K += 1
    elif mask[i] == 2:
        offset = 1
        for val in factor_vars[df2006_clean.columns[i]]:
            new_variable_names.append(df2006_clean.columns[i] + '_' + str(val))
            factor_vars_lookup[df2006_clean.columns[i] + '_' + str(val)] = (df2006_clean.columns[i], offset)
            offset += 1
            K += 1

continuous_variables_averages = {}
for i in xrange(len(mask)):
    if mask[i] == 1:
        # find the average of reported values
        vals = df2006_clean.ix[:,i]
        thesum = 0.
        count = 0.
        for j in xrange(N):
            if not isnull(vals[j]):
                thesum += vals[j]
                count += 1.
        continuous_variables_averages[df2006_clean.columns[i]] = thesum / count

# create a mask to remove rows with income06 missing
inc_mask = np.zeros(N)
for i in xrange(N):
    if not isnull(df2006_clean.ix[i,'income06']):
        inc_mask[i] = 1.
num_with_income06 = sum(inc_mask)

# create variables matrix for the regression.  use factor_weights to populate missing data.
X = np.zeros((num_with_income06, K))
X[:,0] = 1.
for j in xrange(1,K):
    if new_variable_names[j-1] not in factor_vars_lookup:
        # it's a continuous variable
        col = df2006_clean.ix[:,new_variable_names[j-1]].copy()
        for i in xrange(len(col)):
            if isnull(col[i]):
                col[i] = continuous_variables_averages[new_variable_names[j-1]]
        for i in xrange(int(num_with_income06)):
            if inc_mask[i]:
                X[i,j] = col[j]
    else:
        # it's a categorical variable
        (var, num) = factor_vars_lookup[new_variable_names[j-1]]
        col = df2006_clean.ix[:,var].copy()
        for i in xrange(len(col)):
            if isnull(col[i]):
                col[i] = 0.
            elif col[i] == num:
                col[i] = 1.
            else:
                col[i] = 0.
        for i in xrange(int(num_with_income06)):
            if inc_mask[i]:
                X[i,j] = col[j]

# create Y
t = []
for i in xrange(N):
    if inc_mask[i]:
        t.append(df2006_clean.ix[i,'income06'])
Y = np.array(t)

import pickle
fX = open('X.pickle', 'w')
fY = open('Y.pickle', 'w')
pickle.dump(X, fX)
pickle.dump(Y, fY)
fX.close()
fY.close()


#### OK, now again for 2010

# set a mask for determining which columns we'll use and how
# -1 = prediction variable
# 0 = drop
# 1 = keep
# 2 = factorize (we'll keep a dict with the possible values)
# 3 = only in the enhanced model
mask = np.zeros(len(df2010_clean.columns))
N = df2010_clean.shape[0]
for i in xrange(len(mask)):
    mask[23] = -1
    if i in [6,9,10,11,12,13,14,16,21,28,34,43,45,59]:
        mask[i] = 1
    elif i in [2,8,24,25]:
        mask[i] = 2
    elif i in [3,4,15,44]:
        mask[i] = 3

# for factorize variables, what are the allowed values other than 'no answer'?
# we'll leave 'no answer's blank for now and later fill them in with frequency weights
factor_vars = {'wrkstat': [1,2,3,4,5,6,7,8], 'marital': [1,2,3,4,5], 'region': [1,2,3,4,5,6,7,8,9], 'xnorcsiz': [1,2,3,4,5,6,7,8,9,10]}
factor_vars_lookup = {}

# for each factor variable, figure out the frequency weights
factor_weights = {}
factor_counts = {}
for var in factor_vars:
    factor_weights[var] = {}
    factor_counts[var] = {}
    for t in factor_vars[var]:
        factor_counts[var][t] = 0.
for i in xrange(df2010_clean.shape[0]):
    for var in factor_vars:
        t = df2010_clean.ix[i,var]
        if t in factor_vars[var]:
            factor_counts[var][t] += 1
for var in factor_vars:
    m = 0.
    for t in factor_counts[var]:
        m += factor_counts[var][t]
    for t in factor_counts[var]:
        factor_weights[var][t] = factor_counts[var][t] / m
        
K = 1 # start with 1 for a constant term
new_variable_names = []
for i in xrange(len(mask)):
    if mask[i] == 1:
        new_variable_names.append(df2010_clean.columns[i])
        K += 1
    elif mask[i] == 2:
        offset = 1
        for val in factor_vars[df2010_clean.columns[i]]:
            new_variable_names.append(df2010_clean.columns[i] + '_' + str(val))
            factor_vars_lookup[df2010_clean.columns[i] + '_' + str(val)] = (df2010_clean.columns[i], offset)
            offset += 1
            K += 1

continuous_variables_averages = {}
for i in xrange(len(mask)):
    if mask[i] == 1:
        # find the average of reported values
        vals = df2010_clean.ix[:,i]
        thesum = 0.
        count = 0.
        for j in xrange(N):
            if not isnull(vals[j]):
                thesum += vals[j]
                count += 1.
        continuous_variables_averages[df2010_clean.columns[i]] = thesum / count

# create a mask to remove rows with income06 missing
inc_mask = np.zeros(N)
for i in xrange(N):
    if not isnull(df2010_clean.ix[i,'income06']):
        inc_mask[i] = 1.
num_with_income06 = sum(inc_mask)

# create variables matrix for the regression.  use factor_weights to populate missing data.
X = np.zeros((num_with_income06, K))
X[:,0] = 1.
for j in xrange(1,K):
    if new_variable_names[j-1] not in factor_vars_lookup:
        # it's a continuous variable
        col = df2010_clean.ix[:,new_variable_names[j-1]].copy()
        for i in xrange(len(col)):
            if isnull(col[i]):
                col[i] = continuous_variables_averages[new_variable_names[j-1]]
        for i in xrange(int(num_with_income06)):
            if inc_mask[i]:
                X[i,j] = col[j]
    else:
        # it's a categorical variable
        (var, num) = factor_vars_lookup[new_variable_names[j-1]]
        col = df2010_clean.ix[:,var].copy()
        for i in xrange(len(col)):
            if isnull(col[i]):
                col[i] = 0.
            elif col[i] == num:
                col[i] = 1.
            else:
                col[i] = 0.
        for i in xrange(int(num_with_income06)):
            if inc_mask[i]:
                X[i,j] = col[j]

# create Y
t = []
for i in xrange(N):
    if inc_mask[i]:
        t.append(df2010_clean.ix[i,'income06'])
Y = np.array(t)

import pickle
fX = open('X2010.pickle', 'w')
fY = open('Y2010.pickle', 'w')
pickle.dump(X, fX)
pickle.dump(Y, fY)
fX.close()
fY.close()
