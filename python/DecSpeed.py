import timeit
import time
import scipy.sparse as sp
import itertools
import matplotlib.pyplot as plt
import statistics
import io

from H2ZIXY import H2ZIXY
from PauliDecTensor import PauliDecTensor

import pennylane as qml
from pennylane import numpy as np

# Setup Parameters
out = 1
debug = 0
runs = 3
plot = 0

def diagRandom(dim):
	return np.add(np.zeros([dim,dim]),np.diag(np.add(np.random.rand(dim),1.j*np.random.rand(dim))))
def randomMatrix(dim):
	return np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))
def identityMatrix(dim):
	return np.identity(dim)
def sparseRandom(dim):
	return sp.random(dim,dim,density=0.25**dim,format="csr")
def PauliDecSparse(matrix):
	return PauliDecTensor(matrix,sparse=True)

CompareMethods = ["Linear Algebra", "Tensor Sparse", "Tensor Linear", "Penny Lane"]

Methods = {"Linear Algebra": H2ZIXY, "Tensor Sparse": PauliDecSparse, "Tensor Linear": PauliDecTensor, "Penny Lane": qml.pauli_decompose}
MaxSizes = {"Linear Algebra": 6, "Tensor Sparse": 8, "Tensor Linear": 9, "Penny Lane": 7}
Tests = ["Diagonal Matrix", "Unit Matrix", "Random Matrix", "Sparse Matrix"]
TestMatrices = {"Diagonal Matrix": diagRandom, "Unit Matrix": identityMatrix, "Random Matrix": randomMatrix, "Sparse Matrix": sparseRandom}
Results = {}

# Test of speed and stochastic evaluation
if out: print("Speed Test:")
for Test in Tests:
	tab = {}
	if out: print(f"{Test}:")

	with io.open(f"{Test}.dat", "w") as file:
		for Method in CompareMethods:
			outputLine = f"{Method} \n"
			file.write(outputLine)
			if out: print(f"{Method}:")
			tab[Method] = []

			for n in range(1,MaxSizes[Method]):
				outputLine = [f"{n} \t"]
				dim = 2**n
				matrix = TestMatrices[Test](dim)

				if Test == "Sparse Matrix":
					if Method != "Tensor Sparse":
						matrix = np.array(matrix.todense())
				if Method == "Penny Lane":
					matrix = 0.5* (matrix + matrix.conjugate().transpose())

				elapsed = []
				for i in range(runs):
					start_time = time.process_time()
					Methods[Method](matrix)
					elapsed.append(time.process_time() - start_time)
				mean = statistics.mean(elapsed)
				stdev = statistics.stdev(elapsed)
				outputLine.append(f"{mean} \t {stdev} \n")
				file.write("".join(outputLine))

				tab[Method].append(elapsed)
				if out: print("dim",n,": ",elapsed)
			file.write("\n\n")

	Results[Test] = tab


if plot:
	for Test in Tests:
		fig,ax = plt.subplots(figsize=(10,5),dpi=150)
		plt.xlabel('Number of Qubits')
		plt.ylabel('log Computation Time (s)')
		plt.title('Comparison of Computation Time ('+Test+")")
		plt.grid(True)
		for Method in CompareMethods:
			ax.plot(range(1,MaxSizes[Method]),np.log(Results[Test][Method])/np.log(4), 'o-', label=Method)
		plt.legend()
		fig.savefig("plot"+Test+".png",dpi=150)
