import numpy as np
import scipy.sparse as sp
import itertools

debug = 0
out = 0
test = 0

def PauliDecSparse(matrix, PauliStringInit = ""):
# Initialize values
	matrix = sp.csr_array(matrix)
	if debug: print("Mat: ",matrix)
	dim = matrix.shape[0]
	if debug: print("Shape: ",matrix.shape)
	log2dim = int(np.log(dim)/np.log(2))
	decomposition = ""
# Last step
	if log2dim == 0:
		if debug: print("Factor: ",matrix[0,0])
		if matrix[0,0] != 0:
			if debug: print("String: ",PauliStringInit)
			decomposition = str(matrix[0,0])+", "+PauliStringInit
# Submatrices for higher dimension
	if log2dim > 0:
		d2 = int(dim/2)
# Blockmatrix decomposition
		if debug: print("Mat: ",matrix[0:d2,0:d2])
		rest1 = 0.5*(matrix[0:d2,0:d2]+matrix[d2:,d2:])
		restX = 0.5*(matrix[d2:,0:d2]+matrix[0:d2,d2:])
		restY = 1.j*0.5*(matrix[d2:,0:d2]-matrix[0:d2,d2:])
		restZ = 0.5*(matrix[0:d2,0:d2]-matrix[d2:,d2:])
		if debug: print("1: ",rest1)
# Ignore trivial parts of decomposition
		if len(rest1.nonzero()[0]) != 0:
			if debug: print("Nonzeros: ",rest1.nonzero()[0])
			decomposition += PauliDecSparse(rest1,PauliStringInit+"1")
		else:
			if debug: print("Zero Entries")
		if len(restX.nonzero()) != 0:
			decomposition += PauliDecSparse(restX,PauliStringInit+"X")
		if len(restY.nonzero()) != 0:
			decomposition += PauliDecSparse(restY,PauliStringInit+"Y")
		if len(restZ.nonzero()) != 0:
			decomposition += PauliDecSparse(restZ,PauliStringInit+"Z")
	return decomposition

testMat1 = np.array([[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,-1]],dtype=np.cdouble)
testMat2 = np.array([[-1,0],[0,1]],dtype=np.cdouble)

if test:
	decomposition = PauliDecSparse(testMat1)
	if out: print(decomposition)
	decomposition = PauliDecSparse(testMat2)
	if out: print(decomposition)
