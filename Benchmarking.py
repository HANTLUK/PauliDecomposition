import timeit
import time
import scipy.sparse as sp
import itertools
import matplotlib.pyplot as plt
import statistics
import io

from H2ZIXY import H2ZIXY # H2ZIXY Algorithm
from pauli_decomposer import PauliDecomposer # Pauli Decomposer Paper
import cirq
import pennylane as qml
from pennylane import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit.quantum_info.operators import Operator, Pauli
from TFIM import tfimHamiltonian
""" Test of Pauli Decomposition Runtime for different instances for different Algorithms"""

# Setup Parameters
out = 1
debug = 0
stat_runs = 2
stat = 1
timeBarrier = 10

def diagRandom(dim):
	return np.add(np.zeros([dim,dim]),np.diag(np.add(np.random.rand(dim),1.j*np.random.rand(dim))))
def randomMatrix(dim):
	return np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))
def identityMatrix(dim):
	return np.identity(dim)
def sparseRandom(dim):
	return sp.random(dim,dim,density=1./dim,format="csr")
def PauliDecSparse(matrix):
	return PauliDecTensor(matrix,sparse=True)
def symmRandom(dim):
	rand = randomMatrix(dim)
	return np.add(rand,np.transpose(rand))
def hermRandom(dim):
	rand = randomMatrix(dim)
	return np.add(rand,rand.conjugate().transpose())
def oneTerm(dim):
	rand = randomMatrix(2)
	return np.kron(rand,np.eye(int(dim/2)))

CompareMethods = ["Qiskit"]
ExecuteTests = ["rand", "unit"]
# ["tfim", "diag", "herm", "spars", "symm", "rand", "unit", "oneTerm"]
# ["tfim", "diag", "herm", "spars", "symm", "rand", "unit"]

Methods = {"h2zixy": H2ZIXY, "pennylane": qml.pauli_decompose, "Qiskit": SparsePauliOp.from_operator, "Cirq": cirq.pauli_expansion, "PC": PauliDecomposer}
MethodsName = {"h2zixy": "h2", "pennylane": "pl", "Qiskit": "Qk", "PC": "PC"}
MaxSizes = {"h2zixy": 9, "pennylane": 10, "Qiskit": 10, "Cirq": 10, "PC" : 10}
Tests = {"diag": "Diagonal Matrix", "herm" : "Hermitian Matrix", "symm": "Symmetric Matrix", "rand": "Random Matrix", "spars": "Sparse Matrix", "unit": "Unit Matrix", "tfim": "TFIM Hamiltonian", "oneTerm": "One Term"}
TestMatrices = {"diag": diagRandom, "unit": identityMatrix, "rand": randomMatrix, "spars": sparseRandom, "herm" : hermRandom, "symm" : symmRandom, "tfim": tfimHamiltonian, "oneTerm": oneTerm}
Results = {}

# Test of speed and stochastic evaluation
if stat:
	if out: print("Speed Test:")
	for Test in ExecuteTests:
		tab = {}
		if out: print(f"{Tests[Test]}:")

		with io.open(f"{Tests[Test]}.dat", "w") as file:
			for Method in CompareMethods:
				outputLine = f"{MethodsName[Method]} \n"
				file.write(outputLine)
				if out: print(f"{Method}:")
				tab[Method] = []

				for n in range(2,MaxSizes[Method]+1):

					outputLine = [f"{n} \t"]
					dim = 2**n
					matrix = TestMatrices[Test](dim)
					if Test == "spars":
						matrix = np.array(matrix.todense())
					if Method == "pennylane":
						matrix = 0.5* (matrix + matrix.conjugate().transpose())

					elapsed = []
					for i in range(stat_runs):
						start_time = timeit.default_timer()
						if Method == "pennylane" and Test == "spars":
							Methods[Method](matrix)
						else:
							Methods[Method](matrix)
						elapsed.append((timeit.default_timer() - start_time))

					mean = statistics.mean(elapsed)
					outputLine.append(f"{mean} \n")
					file.write("".join(outputLine))

					tab[Method].append(mean)
					if out: print("dim",n,": ",elapsed)
					if mean > timeBarrier:
						break
				file.write("\n\n")

		Results[Test] = tab
