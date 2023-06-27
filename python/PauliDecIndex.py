import numpy as np

def PauliDecIndex(matrix, order, PauliStringInit = ""):
	"""
		Returns the Pauli Decomposition of a square matrix with the given order.

		Iteratively splits tensor factors off and decomposes those smaller matrices.
		This is done using submatrices of the original matrix. The Pauli Strings are
		generated in each step.

		Args:
			matrix: Matrix to be decomposed (Preferrably numpy array)
			order: Order of tensor factors.
			PauliStringInit: For recursive computation.
		Returns:
			decomposition: String of 1XYZ with their factors.
	"""

	matrix = np.array(matrix)
	dim = matrix.shape[0]
	qBitDim = int(np.log(dim)/np.log(2))
	decomposition = []

	if qBitDim == 0:
		if matrix[0,0] != 0.0:
			decomposition = f"{str(matrix[0,0])}, {PauliStringInit}. "

	# Calculates the tensor product coefficients via the sliced submatrices.
	# If one of these components is zero it doesn't have to be decomposed further.

	if qBitDim > 0:
		halfDim = int(2**(qBitDim-1))

		rest1 = 0.5*(matrix[0:halfDim,0:halfDim]+matrix[halfDim:,halfDim:])
		restX = 0.5*(matrix[halfDim:,0:halfDim]+matrix[0:halfDim,halfDim:])
		restY = 1.j*0.5*(matrix[halfDim:,0:halfDim]-matrix[0:halfDim,halfDim:])
		restZ = 0.5*(matrix[0:halfDim,0:halfDim]-matrix[halfDim:,halfDim:])

		matrix = None

		if rest1.any():
			decomposition.append(PauliDecIndex(rest1,order[:-1],f"1{PauliStringInit}"))
		if restX.any():
			decomposition.append(PauliDecIndex(restX,order[:-1],f"X{PauliStringInit}"))
		if restY.any():
			decomposition.append(PauliDecIndex(restY,order[:-1],f"Y{PauliStringInit}"))
		if restZ.any():
			decomposition.append(PauliDecIndex(restZ,order[:-1],f"Z{PauliStringInit}"))

	outputString = "".join(decomposition)
	return outputString
