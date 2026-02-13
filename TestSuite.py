import numpy as np
import math
from typing import List
from TensorizedPauliDecomposition import pauli_decomposition

from qiskit.quantum_info import SparsePauliOp

def test_qiskit(matrix: np.ndarray) -> List[list]:
	"""Decompose a matrix using Qiskit's SparsePauliOp for reference comparison.

	Parameters
	----------
	matrix : np.ndarray
	    Square matrix to decompose.

	Returns
	-------
	list of [PauliList, np.ndarray]
	    ``[pauli_strings, coefficients]`` from Qiskit's decomposition.

	Examples
	--------
	>>> result = test_qiskit(np.eye(2))
	>>> len(result)
	2
	"""
	test_result = SparsePauliOp.from_operator(matrix)
	coeffs_qiskit = test_result.coeffs
	pauli_strings_qiskit = test_result.paulis
	return [pauli_strings_qiskit, coeffs_qiskit]

def test_tpd(matrix: np.ndarray) -> List[list]:
	"""Decompose a matrix using the tensorized Pauli decomposition algorithm.

	Parameters
	----------
	matrix : np.ndarray
	    Square matrix to decompose.

	Returns
	-------
	list of [list of str, list of complex]
	    ``[pauli_strings, coefficients]`` from the TPD algorithm.

	Examples
	--------
	>>> result = test_tpd(np.eye(2))
	>>> len(result)
	2
	"""
	pauli_strings_tpd, coeffs_tpd = pauli_decomposition(matrix)
	return [pauli_strings_tpd, coeffs_tpd]

def random_matrix(dim: int) -> np.ndarray:
	"""Generate a random complex matrix of given dimension.

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

def compare_methods(method1, method2, matrix: np.ndarray) -> bool:
	"""Compare two Pauli decomposition methods for equivalence.

	Runs both methods on the same matrix and checks that the resulting
	Pauli strings match exactly and coefficients agree within tolerance.

	Parameters
	----------
	method1 : callable
	    First decomposition function returning [pauli_strings, coefficients].
	method2 : callable
	    Second decomposition function returning [pauli_strings, coefficients].
	matrix : np.ndarray
	    Square matrix to decompose with both methods.

	Returns
	-------
	bool
	    True if both methods produce the same Pauli strings and
	    coefficients within tolerance (1e-5), False otherwise.

	Examples
	--------
	>>> M = random_matrix(4)
	>>> compare_methods(test_tpd, test_qiskit, M)
	True
	"""
	pauli_strings_tpd, coeffs_tpd = method1(matrix)
	pauli_strings_qiskit, coeffs_qiskit = method2(matrix)
	equal = True
	for x,y in zip(pauli_strings_tpd, pauli_strings_qiskit):
		if str(x) != str(y):
			equal = False
	# Tolerance for floating-point coefficient comparison
	eps = 10**(-5)
	for x,y in zip(coeffs_tpd, coeffs_qiskit):
		if abs(complex(x) - complex(y)) > eps:
			equal = False
	return equal

if __name__ == "__main__":
	test_matrix = random_matrix(4)
	print(compare_methods(test_tpd, test_qiskit, test_matrix))
