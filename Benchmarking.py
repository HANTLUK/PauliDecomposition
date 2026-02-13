import timeit
import time
import scipy.sparse as sp
import itertools
import matplotlib.pyplot as plt
import statistics
import io
from typing import Dict, List

from H2ZIXY import H2ZIXY # H2ZIXY Algorithm
from pauli_decomposer import PauliDecomposer # Pauli Decomposer Paper
import cirq
import pennylane as qml
from pennylane import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit.quantum_info.operators import Operator, Pauli
from TFIM import tfim_hamiltonian
""" Test of Pauli Decomposition Runtime for different instances for different Algorithms"""

# Setup Parameters
OUTPUT_ENABLED = 1
DEBUG_ENABLED = 0
STAT_RUNS = 2
STAT_ENABLED = 1
TIME_BARRIER = 10

def diag_random(dim: int) -> np.ndarray:
	"""Generate a random complex diagonal matrix.

	Parameters
	----------
	dim : int
	    Side length of the square matrix.

	Returns
	-------
	np.ndarray
	    Complex diagonal matrix of shape (dim, dim).

	Examples
	--------
	>>> M = diag_random(4)
	>>> M.shape
	(4, 4)
	"""
	return np.add(np.zeros([dim,dim]),np.diag(np.add(np.random.rand(dim),1.j*np.random.rand(dim))))

def random_matrix(dim: int) -> np.ndarray:
	"""Generate a random complex matrix.

	Parameters
	----------
	dim : int
	    Side length of the square matrix.

	Returns
	-------
	np.ndarray
	    Random complex matrix of shape (dim, dim).

	Examples
	--------
	>>> M = random_matrix(4)
	>>> M.shape
	(4, 4)
	"""
	return np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))

def identity_matrix(dim: int) -> np.ndarray:
	"""Generate an identity matrix.

	Parameters
	----------
	dim : int
	    Side length of the square matrix.

	Returns
	-------
	np.ndarray
	    Identity matrix of shape (dim, dim).

	Examples
	--------
	>>> M = identity_matrix(4)
	>>> np.allclose(M, np.eye(4))
	True
	"""
	return np.identity(dim)

def sparse_random(dim: int) -> sp.csr_matrix:
	"""Generate a random sparse matrix in CSR format.

	Density is set to 1/dim, producing approximately dim non-zero elements.

	Parameters
	----------
	dim : int
	    Side length of the square matrix.

	Returns
	-------
	scipy.sparse.csr_matrix
	    Random sparse matrix of shape (dim, dim).

	Examples
	--------
	>>> M = sparse_random(8)
	>>> M.shape
	(8, 8)
	"""
	return sp.random(dim,dim,density=1./dim,format="csr")

def pauli_dec_sparse(matrix) -> list:
	"""Run Pauli decomposition on a sparse matrix.

	Wrapper that calls ``pauli_decomposition`` with ``sparse=True``.

	Parameters
	----------
	matrix : scipy.sparse.spmatrix
	    Sparse matrix to decompose.

	Returns
	-------
	list
	    Pauli decomposition result from ``pauli_decomposition``.

	Examples
	--------
	>>> M = sparse_random(4)
	>>> result = pauli_dec_sparse(M)
	"""
	return pauli_decomposition(matrix,sparse=True)

def symm_random(dim: int) -> np.ndarray:
	"""Generate a random complex symmetric matrix.

	Constructs M + M^T from a random matrix M.

	Parameters
	----------
	dim : int
	    Side length of the square matrix.

	Returns
	-------
	np.ndarray
	    Symmetric complex matrix of shape (dim, dim).

	Examples
	--------
	>>> M = symm_random(4)
	>>> np.allclose(M, M.T)
	True
	"""
	rand = random_matrix(dim)
	return np.add(rand,np.transpose(rand))

def herm_random(dim: int) -> np.ndarray:
	"""Generate a random Hermitian matrix.

	Constructs M + M^dagger from a random matrix M.

	Parameters
	----------
	dim : int
	    Side length of the square matrix.

	Returns
	-------
	np.ndarray
	    Hermitian matrix of shape (dim, dim).

	Examples
	--------
	>>> M = herm_random(4)
	>>> np.allclose(M, M.conj().T)
	True
	"""
	rand = random_matrix(dim)
	return np.add(rand,rand.conjugate().transpose())

def one_term(dim: int) -> np.ndarray:
	"""Generate a matrix with a single tensor-product term.

	Creates kron(random_2x2, I_{dim/2}), which decomposes into
	exactly one Pauli tensor product term per 2x2 Pauli component.

	Parameters
	----------
	dim : int
	    Side length of the square matrix. Must be even.

	Returns
	-------
	np.ndarray
	    Matrix of shape (dim, dim) with Kronecker product structure.

	Examples
	--------
	>>> M = one_term(4)
	>>> M.shape
	(4, 4)
	"""
	rand = random_matrix(2)
	return np.kron(rand,np.eye(int(dim/2)))

compare_methods = ["Qiskit"]
execute_tests = ["rand", "unit"]
# ["tfim", "diag", "herm", "spars", "symm", "rand", "unit", "oneTerm"]
# ["tfim", "diag", "herm", "spars", "symm", "rand", "unit"]

methods = {"h2zixy": H2ZIXY, "pennylane": qml.pauli_decompose, "Qiskit": SparsePauliOp.from_operator, "Cirq": cirq.pauli_expansion, "PC": PauliDecomposer}
methods_name = {"h2zixy": "h2", "pennylane": "pl", "Qiskit": "Qk", "PC": "PC"}
max_sizes = {"h2zixy": 9, "pennylane": 10, "Qiskit": 10, "Cirq": 10, "PC" : 10}
tests = {"diag": "Diagonal Matrix", "herm" : "Hermitian Matrix", "symm": "Symmetric Matrix", "rand": "Random Matrix", "spars": "Sparse Matrix", "unit": "Unit Matrix", "tfim": "TFIM Hamiltonian", "oneTerm": "One Term"}
test_matrices = {"diag": diag_random, "unit": identity_matrix, "rand": random_matrix, "spars": sparse_random, "herm" : herm_random, "symm" : symm_random, "tfim": tfim_hamiltonian, "oneTerm": one_term}

if __name__ == "__main__":
	results = {}

	# Test of speed and stochastic evaluation
	if STAT_ENABLED:
		if OUTPUT_ENABLED: print("Speed Test:")
		for test_name in execute_tests:
			tab = {}
			if OUTPUT_ENABLED: print(f"{tests[test_name]}:")

			with io.open(f"{tests[test_name]}.dat", "w") as file:
				for method_name in compare_methods:
					output_line = f"{methods_name[method_name]} \n"
					file.write(output_line)
					if OUTPUT_ENABLED: print(f"{method_name}:")
					tab[method_name] = []

					for n in range(2,max_sizes[method_name]+1):

						output_line = [f"{n} \t"]
						dim = 2**n
						matrix = test_matrices[test_name](dim)
						if test_name == "spars":
							matrix = np.array(matrix.todense())
						if method_name == "pennylane":
							matrix = 0.5* (matrix + matrix.conjugate().transpose())

						elapsed = []
						for i in range(STAT_RUNS):
							start_time = timeit.default_timer()
							if method_name == "pennylane" and test_name == "spars":
								methods[method_name](matrix)
							else:
								methods[method_name](matrix)
							elapsed.append((timeit.default_timer() - start_time))

						mean = statistics.mean(elapsed)
						output_line.append(f"{mean} \n")
						file.write("".join(output_line))

						tab[method_name].append(mean)
						if OUTPUT_ENABLED: print("dim",n,": ",elapsed)
						if mean > TIME_BARRIER:
							break
					file.write("\n\n")

			results[test_name] = tab
