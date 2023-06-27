import scipy.sparse as sp
import time
import psutil

import pennylane as qml
from pennylane import numpy as np

from PauliDecTensor import PauliDecTensor

out = 1
timing = 1
memory = 1

CompareMethods = [["Tensor",PauliDecTensor],
				  ["Penny Lane",qml.pauli_decompose]]

# Test correct computation
if out: print("Test of Correctness: ")

testMat1 = np.array([[1,0,0,0]
					,[0,-1,0,0]
					,[0,0,0,0]
					,[0,0,0,0]],dtype=np.cdouble)
testMat2 = np.array([[-1,0]
					,[0,1]],dtype=np.cdouble)

for Name,Method in CompareMethods:
	if out: print(f"{Name}:")
	if timing: start_time = time.process_time()
	decomposition = Method(testMat1)
	if timing: elapsed = time.process_time() - start_time
	if out: print(f"Time: {elapsed}")
	if out: print(decomposition)
	if timing: start_time = time.process_time()
	decomposition = Method(testMat2)
	if timing: elapsed = time.process_time() - start_time
	if out: print(f"Time: {elapsed}")
	if out: print(decomposition)
if memory:
	if out: print("Memory Test:")
	n = 10
	dim = 2**n
	print(psutil.Process().memory_info().rss / (1024*1024))
	if timing: start_time = time.process_time()
	testMat3 = np.random.rand(dim,dim)
	if timing: elapsed = time.process_time() - start_time
	if out: print(f"Time: {elapsed}")
	print(psutil.Process().memory_info().rss / (1024*1024))
	decomposition = PauliDecTensor(testMat3)
	print(psutil.Process().memory_info().rss / (1024*1024))
