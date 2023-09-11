import scipy.sparse as sp
import time
import psutil
import math

from scipy.sparse import dok_matrix
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
from poisson import Grid

import pennylane as qml
from pennylane import numpy as np

from PauliDecTensor import PauliDecTensor

from qiskit.quantum_info import SparsePauliOp

def PadMatrix(matrix,sparse=False):
	matDim = matrix.shape[0]
	qBitDim = math.ceil(np.log(matDim)/np.log(2))

	# Pad, if dimension is not a power of 2

	padDim = 2**qBitDim - matDim
	if padDim:
		if sparse:
			indxptr = np.pad(matrix.indptr, ((0, padDim), (0, padDim)))
			matrix = csr_matrix((matrix.data, matrix.indices, indxptr))
		else:
			matrix = np.pad(matrix, ((0,padDim), (0,padDim)))
	return matrix

out = 1
timing = 1
memory = 1

CompareMethods = [["Tensor",PauliDecTensor],
				  ["Qiskit",SparsePauliOp.from_operator]]

# Test correct computation
# Generate Test Matrices

testMat1 = np.array([[1,0,0,0]
					,[0,-1,0,0]
					,[0,0,0,0]
					,[0,0,0,0]],dtype=np.cdouble)
testMat2 = np.array([[-1,0]
					,[0,1]],dtype=np.cdouble)

testMat4 = np.array([[-0.43658111, -4.28660705, 0, 0],
					[-4.28660705,12.15,-7.82623792,0],
					[0,-7.82623792,19.25,0],
					[0,0,0,0]],dtype=np.cdouble)

grid = Grid(stepSize = 0.08)
grid.decompose()
testMat3, F = grid.assembleSystem()

TestMatrices = [testMat1,testMat2,testMat4]

if out: print("Test of Correctness: ")

for Name,Method in CompareMethods:
	for Matrix in TestMatrices:
		if out: print(f"{Name}:")
		if timing: start_time = time.process_time()
		decomposition = Method(Matrix)
		if timing: elapsed = time.process_time() - start_time
		if out: print(f"Time: {elapsed}")
		if out:	print(decomposition)
