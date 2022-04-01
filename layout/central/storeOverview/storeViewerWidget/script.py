import numpy as np
from numpy.linalg import *


dist = np.array([228.52, 440.12])   # d = 211.6
longH = np.array([172, 383.60]) # d = 211.6
longA = np.array([192.37, 436.71])  # d = 244.34



dDist = dist[1] - dist[0]
dLongH = longH[1] - longH[0]
dLongA = longA[1] - longA[0]

# dLongH/dDist
dLD = dLongH/dDist
print(dLD)

