import numpy as np
import scipy.sparse as sp

def PauliDecTensor(matrix, sparse=False, PauliStringInit=""):
	"""
		Returns the Pauli Decomposition of a square matrix with the given order.

		Iteratively splits tensor factors off and decomposes those smaller
		matrices. This is done using submatrices of the original matrix.
		The Pauli Strings are generated in each step.

		Args:
			matrix: Matrix to be decomposed (Preferrably numpy array / Sparse).
			sparse: If Matrix is in sparse format.
			PauliStringInit: For recursive computation.
		Returns:
			decomposition: String of 1XYZ with their factors.
	"""

	matDim = matrix.shape[0]
	qBitDim = int(np.log(matDim)/np.log(2))
	decomposition = []

	if qBitDim == 0:
		if matrix[0,0] != 0.0:
			decomposition = [f"{str(matrix[0,0])}, {PauliStringInit}. "]

	# Calculates the tensor product coefficients via the sliced submatrices.
	# If one of these components is zero that coefficient is ignored.

	if qBitDim > 0:
		halfDim = int(2**(qBitDim-1))

		coeff1 = 0.5*(matrix[0:halfDim, 0:halfDim]
						+ matrix[halfDim:, halfDim:])
		coeffX = 0.5*(matrix[halfDim:, 0:halfDim]
						+ matrix[0:halfDim, halfDim:])
		coeffY = 1.j*0.5*(matrix[halfDim:, 0:halfDim]
						- matrix[0:halfDim, halfDim:])
		coeffZ = 0.5*(matrix[0:halfDim, 0:halfDim]
						- matrix[halfDim:, halfDim:])

		coefficients = {"1": coeff1, "X": coeffX, "Y": coeffY, "Z": coeffZ}

		matrix = None

		if sparse:
			for c in coefficients:
				mat = coefficients[c]
				if  len(mat.nonzero()[0]) != 0:
					subDec = PauliDecTensor(mat,sparse,f"{PauliStringInit}{c}")
					decomposition.append(subDec)
		else:
			for c in coefficients:
				mat = coefficients[c]
				if mat.any():
					subDec = PauliDecTensor(mat,sparse,f"{PauliStringInit}{c}")
					decomposition.append(subDec)

	outputString = "".join(decomposition)
	return outputString
