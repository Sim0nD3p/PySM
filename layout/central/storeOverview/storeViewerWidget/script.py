import numpy as np
from numpy.linalg import *

print('hello world')
u1 = np.vstack(np.array([2, 1, 0, 4]))
u2 = np.vstack(np.array([1, 0, 1, 3]))
u3 = np.vstack(np.array([1, 2, 1, 0]))

w1 = u1
w2 = u2 - np.vdot(w1, u2)/np.square(norm(w1))*w1
w3 = u3 - np.vdot(w1, u3)/np.square(norm(w1))*w1 - np.vdot(w2, u3)/np.square(norm(w2))*w2
# print(w2)
# print(w3)

result = np.array([
    [w1/norm(w1)],
    [w2/norm(w2)],
    [w3/norm(w3)]
])
# print(w1/norm(w1))
# print(w2/norm(w2))
# print(w3/norm(w3))
# print(result.transpose())

w2 = np.vstack(np.array([0, 1, 2])) - 0.5*np.vstack(np.array([1, 1, 0])) - 2/5*np.vstack(np.array([-0.5, 0.5, 0]))
w1 = np.vstack(np.array([-1/2, 1/2, 0]))
print(norm(w1))
