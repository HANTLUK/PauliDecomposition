import numpy as np
import itertools

debug = 0
out = 1

def PauliDecImproved(matrix, PauliStringInit = ""):
# Initialize values
	matrix = np.array(matrix)
	dim = matrix.shape[0]
	log2dim = int(np.log(dim)/np.log(2))
	decomposition = ""
# Iterate over Possible Pauli Strings
# Submatrices for higher dimension
	if log2dim == 0:
		if matrix[0,0] != 0:
			decomposition = str(matrix[0,0])+", "+PauliStringInit
	if log2dim > 0:
		d2 = int(dim/2)
# Blockmatrix decomposition
		rest1 = 0.5*(matrix[0:d2,0:d2]+matrix[d2:,d2:])
		restX = 0.5*(matrix[d2:,0:d2]+matrix[0:d2,d2:])
		restY = 1.j*0.5*(matrix[d2:,0:d2]-matrix[0:d2,d2:])
		restZ = 0.5*(matrix[0:d2,0:d2]-matrix[d2:,d2:])
# Ignore trivial parts of decomposition
		if rest1.any() != 0:
			decomposition += PauliDecImproved(rest1,PauliStringInit+"1")
		if restX.any() != 0:
			decomposition += PauliDecImproved(restX,PauliStringInit+"X")
		if restY.any() != 0:
			decomposition += PauliDecImproved(restY,PauliStringInit+"Y")
		if restZ.any() != 0:
			decomposition += PauliDecImproved(restZ,PauliStringInit+"Z")
	return decomposition
