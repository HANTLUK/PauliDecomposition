import numpy as np
import math
from typing import List
from TensorizedPauliDecomposition import pauli_decomposition

from qiskit.quantum_info import SparsePauliOp

def decompose_with_qiskit(matrix: np.ndarray) -> List[list]:
	"""Decompose a matrix using Qiskit's SparsePauliOp for reference comparison.

	This wrapper function calls Qiskit's built-in Pauli decomposition to
	provide a reference implementation for validating our TPD algorithm.

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
	>>> result = decompose_with_qiskit(np.eye(2))
	>>> len(result)
	2
	"""
	test_result = SparsePauliOp.from_operator(matrix)
	coeffs_qiskit = test_result.coeffs
	pauli_strings_qiskit = test_result.paulis
	return [pauli_strings_qiskit, coeffs_qiskit]

def decompose_with_tpd(matrix: np.ndarray) -> List[list]:
	"""Decompose a matrix using the tensorized Pauli decomposition algorithm.

	This wrapper function calls our TPD implementation to produce a Pauli
	decomposition that can be compared against reference implementations.

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
	>>> result = decompose_with_tpd(np.eye(2))
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
	>>> compare_methods(decompose_with_tpd, decompose_with_qiskit, M)
	True
	"""
	pauli_strings_tpd, coeffs_tpd = method1(matrix)
	pauli_strings_qiskit, coeffs_qiskit = method2(matrix)
	equal = True

	# Verify that Pauli strings match exactly between both methods.
	# Both implementations should produce the same operator basis (same set
	# of Pauli tensor products), so any mismatch indicates an error.
	for x,y in zip(pauli_strings_tpd, pauli_strings_qiskit):
		if str(x) != str(y):
			equal = False

	# Verify that coefficients agree within numerical tolerance.
	# Different implementations may use different numerical backends
	# (NumPy, SciPy sparse, etc.) that introduce slight floating-point
	# variations. 1e-5 is sufficient precision for quantum simulation
	# while accommodating these implementation differences.
	eps = 10**(-5)
	for x,y in zip(coeffs_tpd, coeffs_qiskit):
		if abs(complex(x) - complex(y)) > eps:
			equal = False
	return equal

if __name__ == "__main__":
	# Run a quick validation: decompose a random 4x4 matrix with both TPD
	# and Qiskit, then verify equivalence.
	test_matrix = random_matrix(4)
	print(compare_methods(decompose_with_tpd, decompose_with_qiskit, test_matrix))
