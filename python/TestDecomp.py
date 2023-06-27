import timeit
import time
import scipy.sparse as sp
import itertools
import matplotlib.pyplot as plt
from PauliDec import PauliDec
from PauliDecTrace import PauliDecTrace
from PauliDecLinA import PauliDecLinA
from PauliDecSparse import PauliDecSparse
from PauliDecTensor import PauliDecTensor
import pennylane as qml
from pennylane import numpy as np

# Setup Parameters
out = 1
debug = 0
test = 0
runs = 1
speed = 1
diag = 1
unit = 1
rand = 1
sparse = 1

def diagRandom(dim):
	return np.add(np.zeros([dim,dim]),np.diag(np.add(np.random.rand(dim),1.j*np.random.rand(dim))))
def randomMatrix(dim):
	return np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))
def identityMatrix(dim):
	return np.identity(dim)
def sparseRandom(dim):
	return sp.random(dim,dim,density=0.25**dim,format="csr")

CompareMethods = ["Trace", "Linear Algebra", "Sparse", "Tensor Linear", "Penny Lane"]

Methods = {"Partial Trace": PauliDec, "Trace": PauliDecTrace, "Linear Algebra": PauliDecLinA, "Sparse": PauliDecSparse, "Tensor Linear": PauliDecTensor, "Penny Lane": qml.pauli_decompose}
MaxSizes = {"Partial Trace": 10, "Trace": 7, "Linear Algebra": 6, "Sparse": 7, "Tensor Linear": 10, "Tensor Product (C++)": 13, "Penny Lane": 8}
Tests = {"Diagonal Matrix": diag, "Unit Matrix": unit, "Random Matrix": rand, "Sparse Matrix": sparse}
TestMatrices = {"Diagonal Matrix": diagRandom, "Unit Matrix": identityMatrix, "Random Matrix": randomMatrix, "Sparse Matrix": sparseRandom}
Results = {}

# Test of Speed for Random Matrices or unit matrix
if speed:
	if out: print("Speed Test \n")
	for Test in Tests:
		tab = {}
		if Tests[Test]:
			if out: print(Test,":")
			for Method in CompareMethods:
				if out: print(Method+":")
				tab[Method] = []
				for n in range(1,MaxSizes[Method]):
					dim = 2**n
					if debug: print("Dim: ",dim)
					matrix = TestMatrices[Test](dim)
					if Test == "Sparse Matrix":
						if Method != "Sparse":
							matrix = np.array(matrix.todense())
					if Method == "Penny Lane":
						matrix = 0.5* (matrix + matrix.conjugate().transpose())
					if debug: print("Matrix: ",matrix)
					if debug: print("Shape: ",matrix.shape)
					start_time = time.process_time()
					for i in range(runs):
						Methods[Method](matrix)
					elapsed = time.process_time() - start_time
					if elapsed == 0.0:
						elapsed = 0.01
					tab[Method].append(elapsed/float(runs))
					if out: print("dim",n,": ",elapsed)
			Results[Test] = tab

if rand:
	Results["Random Matrix"]["Tensor Product (C++)"] = [0.000000100000000, 0.000000090000000, 0.000000310000000, 0.000001250000000, 0.000005330000000, 0.000023670000000, 0.000140970000000, 0.000428290000000, 0.001826890000000, 0.007680690000000, 0.032192420000000, 0.135278340000000]
if diag:
	Results["Diagonal Matrix"]["Tensor Product (C++)"] = [0.000000030000000, 0.000000110000000, 0.000000160000000, 0.000000890000000, 0.000001210000000, 0.000003780000000, 0.000015080000000, 0.000057980000000, 0.000277650000000, 0.000870320000000, 0.003451000000000, 0.013676140000000]
if unit:
	Results["Unit Matrix"]["Tensor Product (C++)"] = [0.000000020000000, 0.000000040000000, 0.000000130000000, 0.000000230000000, 0.000000900000000, 0.000002480000000, 0.000008720000000, 0.000035760000000, 0.000185310000000, 0.000574910000000, 0.002341480000000, 0.009069320000000]
if sparse:
	Results["Sparse Matrix"]["Tensor Product (C++)"] = [0.000000020000000, 0.000000080000000, 0.000000290000000, 0.000000830000000, 0.000001780000000, 0.000005240000000, 0.000017970000000, 0.000095430000000, 0.000253960000000, 0.000946400000000, 0.003597080000000, 0.014079320000000]

for Test in Tests:
	if Tests[Test]:
		fig,ax = plt.subplots(figsize=(10,5),dpi=150)
		plt.xlabel('Number of Qubits')
		plt.ylabel('log Computation Time (s)')
		plt.title('Comparison of Computation Time ('+Test+")")
		plt.grid(True)
		for Method in CompareMethods:
			ax.plot(range(1,MaxSizes[Method]),np.log(Results[Test][Method])/np.log(4), 'o-', label=Method)
		# Method = "Tensor Product (C++)"
		# ax.plot(range(1,MaxSizes[Method]),np.log(Results[Test][Method])/np.log(4), 'o-', label=Method)
		plt.legend()
		fig.savefig("plot"+Test+".png",dpi=150)
