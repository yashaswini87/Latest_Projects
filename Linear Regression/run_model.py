from homework_03.src import utils
from homework_03.src import linear_reg
from homework_03.src import simulator
from homework_03.src import cross_validator
import pickle
import numpy as np
import numpy.linalg as la

fX = open('X.pickle', 'r')
fY = open('Y.pickle', 'r')
X = pickle.load(fX)
Y = pickle.load(fY)
fX.close()
fY.close()
fX10 = open('X2010.pickle', 'r')
fY10 = open('Y2010.pickle', 'r')
X10 = pickle.load(fX10)
Y10 = pickle.load(fY10)
fX10.close()
fY10.close()

w = linear_reg.fit(X, Y, method='pinv', cutoff=0.1)
#w = linear_reg.fit(X, Y, delta=5)

#print w
#print la.norm(np.dot(X, w) - Y) / la.norm(Y)
newY = np.dot(X, w)

for i in range(len(newY)):
    print newY[i]