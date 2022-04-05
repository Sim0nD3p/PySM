import numpy as np
from numpy.linalg import *


dist = np.array([228.52, 440.12])   # distance tube
longH = np.array([172, 383.60]) # longueur tube horizontal
longA = np.array([192.37, 436.71])  # longueur tube vertical



dDist = dist[1] - dist[0]
dLongH = longH[1] - longH[0]
dLongA = longA[1] - longA[0]

print('dDist:', dDist, ' dH:', dLongH, ' dA:', dLongA)

print(172-228.52)
aA = dLongA/dDist
print('dA/dDist=', aA)
print(longA[1] - aA*dist[1])
# dLongH/dDist
dLD = dDist/dLongH
print(dLD)

