import numpy as np
import math
from TensorizedPauliDecomposition import pauli_decomposition

from qiskit.quantum_info import SparsePauliOp

def test_qiskit(matrix):
	test_result = SparsePauliOp.from_operator(matrix)
	coeffs_qiskit = test_result.coeffs
	pauli_strings_qiskit = test_result.paulis
	return [pauli_strings_qiskit, coeffs_qiskit]

def test_tpd(matrix):
	pauli_strings_tpd, coeffs_tpd = pauli_decomposition(matrix)
	return [pauli_strings_tpd, coeffs_tpd]

def random_matrix(dim):
	return np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))

def compare_methods(method1, method2, matrix):
	pauli_strings_tpd, coeffs_tpd = method1(matrix)
	pauli_strings_qiskit, coeffs_qiskit = method2(matrix)
	equal = True
	for x,y in zip(pauli_strings_tpd, pauli_strings_qiskit):
		if str(x) != str(y):
			equal = False
	eps = 10**(-5)
	for x,y in zip(coeffs_tpd, coeffs_qiskit):
		if abs(complex(x) - complex(y)) > eps:
			equal = False
	return equal

if __name__ == "__main__":
	test_matrix = random_matrix(4)
	print(compare_methods(test_tpd, test_qiskit, test_matrix))
