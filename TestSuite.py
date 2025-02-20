import numpy as np
import math
from TensorizedPauliDecomposition import PauliDecomposition

from qiskit.quantum_info import SparsePauliOp

def test2(matrix):
	testResult2 = SparsePauliOp.from_operator(matrix)
	coeffs2 = testResult2.coeffs
	list2 = testResult2.paulis
	return [list2,coeffs2]

def test1(matrix):
	list1, coeffs1 = PauliDecomposition(matrix)
	return [list1,coeffs1]

def randomMatrix(dim):
	return np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))

testMatrix = randomMatrix(4)

def comparison(method1, method2, matrix):
	list1,coeffs1 = method1(matrix)
	list2,coeffs2 = method2(matrix)
	equal = True
	for x,y in zip(list1,list2):
		if str(x) != str(y):
			equal = False
	eps = 10**(-5)
	for x,y in zip(coeffs1,coeffs2):
		if abs(complex(x) - complex(y)) > eps:
			equal = False
	return equal

print(comparison(test1,test2,testMatrix))
