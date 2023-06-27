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
