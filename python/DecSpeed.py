import timeit
import time
import scipy.sparse as sp
import itertools
import matplotlib.pyplot as plt
import statistics
import io

from H2ZIXY import H2ZIXY
from PauliDecTrace import PauliDecTrace_R
from PauliDecTensor import PauliDecTensor
from PCDecomposer import PCDecomposer_R

import cirq
import pennylane as qml
from pennylane import numpy as np

from qiskit.quantum_info import SparsePauliOp
from qiskit.quantum_info.operators import Operator, Pauli

from TFIM import tfimHamiltonian

# Setup Parameters
out = 1
debug = 0
stat_runs = 4
stat = 1
runs = 2
plot = 0
extremes = 0

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
def symmRandom(dim):
	rand = diagRandom(dim)
	return np.add(rand,np.transpose(rand))
def hermRandom(dim):
	rand = diagRandom(dim)
	return np.add(rand,rand.conjugate().transpose())

CompareMethods = ["h2zixy", "h2zixyTr", "TensorS", "TensorL", "pennylane", "Qiskit", "PC", "PC(d)"]
ExecuteTests = ["tfim", "diag", "herm", "spars", "symm", "rand", "unit"]

# h2zixy .
# qiskit .
# cirq X
# qutip X
# openFermion X
# Strawberry Fields X
# Penny Lane .
# PauliComposer X

Methods = {"h2zixy": H2ZIXY, "TensorS": PauliDecSparse, "TensorL": PauliDecTensor, "pennylane": qml.pauli_decompose, "Qiskit": SparsePauliOp.from_operator, "h2zixyTr": PauliDecTrace_R, "Cirq": cirq.pauli_expansion, "PC": PCDecomposer_R}
MethodsName = {"h2zixy": "h2", "h2zixyTr": "h2(Tr)", "TensorL": "T", "TensorS": "T(Sp)", "pennylane": "pl", "Qiskit": "Qk", "PC": "PC", "PC(d)": "PC(d)"}
MaxSizes = {"h2zixy": 10, "TensorS": 10, "TensorL": 10, "pennylane": 10, "Qiskit": 10, "h2zixyTr": 10, "Cirq": 10, "PC" : 10}
Tests = {"diag": "Diagonal Matrix", "herm" : "Hermitian Matrix", "symm": "Symmetric Matrix", "rand": "Random Matrix", "spars": "Sparse Matrix", "unit": "Unit Matrix", "tfim": "TFIM Hamiltonian"}
TestMatrices = {"diag": diagRandom, "unit": identityMatrix, "rand": randomMatrix, "spars": sparseRandom, "herm" : hermRandom, "symm" : symmRandom, "tfim": tfimHamiltonian}
Results = {}

if extremes:
	dim = 2**15
	start_time = timeit.default_timer()
	PauliDecSparse(sp.random(dim,dim,density=0.25**dim,format="csr"))
	if out: print(timeit.default_timer() - start_time)

herm_PC = [0.0004, 0.0021, 0.012, 0.078, 0.56, 4.24]
rand_PC = [0.0005, 0.0021, 0.012, 0.078, 0.55, 4.06]
symm_PC = [0.0003, 0.0010, 0.0058, 0.036, 0.24, 1.78]
diag_PC = [0.0001, 0.0002, 0.0006, 0.0018, 0.0068, 0.025, 0.094, 0.37, 1.49]


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

				if Method == "PC(d)":
					for n in range(2,10):
						if Test == "herm":
							mean = herm_PC[n-2]
							stdev = 0
						elif Test == "symm":
							mean = symm_PC[n-2]
							stdev = 0
						elif Test == "diag":
							mean = diag_PC[n-2]
							stdev = 0
						elif Test == "rand":
							mean = rand_PC[n-2]
							stdev = 0
						else:
							break
						outputLine = [f"{n} \t {mean} \t {stdev} \n"]
						file.write("".join(outputLine))
						if mean > 1.5:
							break
					break

				for n in range(2,MaxSizes[Method]+1):

					outputLine = [f"{n} \t"]
					dim = 2**n
					matrix = TestMatrices[Test](dim)

					if Test == "spars":
						if Method != "TensorS":
							matrix = np.array(matrix.todense())
					if Method == "pennylane":
						matrix = 0.5* (matrix + matrix.conjugate().transpose())
					if Method == "Cirq":
						matrix = cirq.MatrixGate(matrix)

					elapsed = []
					for i in range(stat_runs):
						start_time = timeit.default_timer()
						for j in range(runs):
							Methods[Method](matrix)
						elapsed.append((timeit.default_timer() - start_time)/float(runs))
					mean = statistics.mean(elapsed)
					stdev = statistics.stdev(elapsed)
					outputLine.append(f"{mean} \t {stdev} \n")
					file.write("".join(outputLine))

					tab[Method].append(mean)
					if out: print("dim",n,": ",elapsed)
					if mean > 1.5:
						break
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
		fig.savefig("PyPlot/PyPlot"+Test+".png",dpi=150)
