import scipy.sparse as sp
import time
import psutil
import numpy as np

from PauliDecTensor import PauliDecTensor

if out: print("Memory Test:")
n = 8
dim = 2**n
print(psutil.Process().memory_info().rss / (1024*1024))
testMat3 = np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))
print(psutil.Process().memory_info().rss / (1024*1024))
decomposition = PauliDecTensor(testMat3)
print(psutil.Process().memory_info().rss / (1024*1024))
