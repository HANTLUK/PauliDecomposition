import numpy as np
import timeit
import scipy.sparse as sp
import itertools
import matplotlib.pyplot as plt
from PauliDec import PauliDec
from PauliDecTrace import PauliDecTrace
from PauliDecLinA import PauliDecLinA
from PauliDecSparse import PauliDecSparse
from PauliDecImproved import PauliDecImproved

# Setup Parameters
out = 1
debug = 0
test = 0
runs = 1
speed = 1
diag = 0
unit = 0
rand = 0
sparse = 1

def diagRandom(dim):
	return np.add(np.zeros([dim,dim]),np.diag(np.add(np.random.rand(dim),1.j*np.random.rand(dim))))
def randomMatrix(dim):
	return np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))
def identityMatrix(dim):
	return np.identity(dim)
def sparseRandom(dim):
	return sp.random(dim,dim,density=0.25**dim,format="csr")

CompareMethods = ["Partial Trace", "Trace", "Linear Algebra", "Sparse", "Tensor Linear"]

Methods = {"Partial Trace": PauliDec, "Trace": PauliDecTrace, "Linear Algebra": PauliDecLinA, "Sparse": PauliDecSparse, "Tensor Linear": PauliDecImproved}
MaxSizes = {"Partial Trace": 10, "Trace": 8, "Linear Algebra": 6, "Sparse": 8, "Tensor Linear": 8, "Tensor Product (c++)": 13}
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
					start_time = timeit.default_timer()
					matrix = TestMatrices[Test](dim)
					if Test == "Sparse Matrix":
						if Method != "Sparse":
							matrix = np.array(matrix.todense())
					if debug: print("Matrix: ",matrix)
					if debug: print("Shape: ",matrix.shape)
					for i in range(runs):
						Methods[Method](matrix)
					elapsed = timeit.default_timer() - start_time
					tab[Method].append(elapsed)
					if out: print("dim",n,": ",elapsed)
			Results[Test] = tab

if rand:
	Results["Random Matrix"]["Tensor Product (c++)"] = [0.000000130000000, 0.000000060000000, 0.000000260000000, 0.000001140000000, 0.000005070000000, 0.000022110000000, 0.000094000000000, 0.000399590000000, 0.001710040000000, 0.007222440000000, 0.030391740000000, 0.126972590000000]

for Test in Tests:
	if Tests[Test]:
		fig,ax = plt.subplots(figsize=(7,5),dpi=150)
		plt.xlabel('Number of Qubits')
		plt.ylabel('log Computation Time (s)')
		plt.title('Comparison of Computation Time ('+Test+")")
		plt.grid(True)
		for Method in CompareMethods:
			ax.plot(range(1,MaxSizes[Method]),np.log(Results[Test][Method])/np.log(4), 'o-', label=Method)
		if rand:
			Method = "Tensor Product (c++)"
			Test = "Random Matrix"
			ax.plot(range(1,MaxSizes[Method]),np.log(Results[Test][Method])/np.log(4), 'o-', label=Method)
		plt.legend()
		fig.savefig("plot"+Test+".png",dpi=150)

runs = 1
test = 0
out = 1
acc = 0
CompareMethods = []

# Tests of Correct Computation
if acc:
	if out: print("Test of Correctness")
	testMat1 = np.array([[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,-1]],dtype=np.cdouble)
	testMat2 = np.array([[-1,0],[0,1]],dtype=np.cdouble)

	for Method in CompareMethods:
		if test: print(Method)
		decomposition = Methods[Method](testMat1)
		if out: print(Method+":")
		for n in decomposition:
			if out: print(n)

	for i in range(runs):
		rand = np.add(np.random.rand(4,4),1.j*np.random.rand(4,4))
		for Method in CompareMethods:
			decomposition = Methods[Method](rand)
			if out: print(Method+":")
			for n in decomposition:
				if out: print(n)
