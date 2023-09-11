import numpy as np
import scipy.sparse as sp
import math

def PauliDecomposition(matrix,sparse=False,PauliStringInit="",output="Lists"):
	"""
		Computes the Pauli decomposition of a square matrix.

		Iteratively splits tensor factors off and decomposes those smaller
		matrices. This is done using submatrices of the original matrix.
		The Pauli strings are generated in each step.

		Args:
			matrix: Matrix to be decomposed
					(Preferrably numpy array/scipysparse).
			output: How the output should be generated.
			sparse: Whether matrix is in sparse format.
			PauliStringInit: For recursive computation.

		Returns:
			decomposition/outString: String of 1XYZ with their factors.
	"""

	matDim = matrix.shape[0]
	qBitDim = math.ceil(np.log(matDim)/np.log(2))

	# Pad, if dimension is not a power of 2

	padDim = 2**qBitDim - matDim
	if padDim != 0:
		if sparse:
			indxptr = np.pad(matrix.indptr, ((0, padDim), (0, padDim)))
			matrix = csr_matrix((matrix.data, matrix.indices, indxptr))
		else:
			matrix = np.pad(matrix, ((0,padDim), (0,padDim)))
	decomposition = []

	if output == "Lists":
		Strings = []
		Coeffs = []


	# Output for dimension 1

	if qBitDim == 0:
		if matrix[0,0] != 0.0:
			if output == "Lists":
				Strings.append(PauliStringInit)
				try:
					Coeffs.append(matrix[0,0])
				except:
					Coeffs.append(matrix[0,0].numpy())
			else:
				decomposition = [f"{matrix[0,0]}, {PauliStringInit}. "]

	# Calculates the tensor product coefficients via the sliced submatrices.
	# If one of these components is zero that coefficient is ignored.

	if qBitDim > 0:
		halfDim = int(2**(qBitDim-1))

		coeff1 = 0.5*(matrix[0:halfDim, 0:halfDim]
						+ matrix[halfDim:, halfDim:])
		coeffX = 0.5*(matrix[halfDim:, 0:halfDim]
						+ matrix[0:halfDim, halfDim:])
		coeffY = -1.j*0.5*(matrix[halfDim:, 0:halfDim]
						- matrix[0:halfDim, halfDim:])
		coeffZ = 0.5*(matrix[0:halfDim, 0:halfDim]
						- matrix[halfDim:, halfDim:])

		coefficients = {"I": coeff1, "X": coeffX, "Y": coeffY, "Z": coeffZ}

		matrix = None

		# Recursion for the Submatrices

		for c in coefficients:
			mat = coefficients[c]
			if sparse:
				nonZero = len(mat.nonzero()[0])
			else:
				nonZero = mat.any()
			# If zero, no branching
			if nonZero != 0:
				subDec = PauliDecomposition(mat,sparse,f"{PauliStringInit}{c}",output)
				if output == "Lists":
					Strings.extend(subDec[0])
					Coeffs.extend(subDec[1])
				else:
					decomposition.append(subDec)

	if output == "Lists":
		return [Strings,Coeffs]
	else:
		outputString = "".join(decomposition)
		return outputString
