import numpy as np
import scipy.sparse as sp
import math

def pauli_decomposition(matrix, sparse=False, pauli_string_init="", output="Lists"):
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
			pauli_string_init: For recursive computation.

		Returns:
			decomposition/output_string: String of 1XYZ with their factors.
	"""

	mat_dim = matrix.shape[0]
	qubit_dim = math.ceil(np.log(mat_dim)/np.log(2))

	# Pad, if dimension is not a power of 2

	pad_dim = 2**qubit_dim - mat_dim
	if pad_dim != 0:
		if sparse:
			indxptr = np.pad(matrix.indptr, ((0, pad_dim), (0, pad_dim)))
			matrix = csr_matrix((matrix.data, matrix.indices, indxptr))
		else:
			matrix = np.pad(matrix, ((0, pad_dim), (0, pad_dim)))
	decomposition = []

	if output == "Lists":
		strings = []
		coeffs = []


	# Output for dimension 1

	if qubit_dim == 0:
		if matrix[0,0] != 0.0:
			if output == "Lists":
				strings.append(pauli_string_init)
				try:
					coeffs.append(matrix[0,0])
				except:
					coeffs.append(matrix[0,0].numpy())
			else:
				decomposition = [f"{matrix[0,0]}, {pauli_string_init}. "]

	# Calculates the tensor product coefficients via the sliced submatrices.
	# If one of these components is zero that coefficient is ignored.

	if qubit_dim > 0:
		half_dim = int(2**(qubit_dim-1))

		coeff1 = 0.5*(matrix[0:half_dim, 0:half_dim]
						+ matrix[half_dim:, half_dim:])
		coeffX = 0.5*(matrix[half_dim:, 0:half_dim]
						+ matrix[0:half_dim, half_dim:])
		coeffY = -1.j*0.5*(matrix[half_dim:, 0:half_dim]
						- matrix[0:half_dim, half_dim:])
		coeffZ = 0.5*(matrix[0:half_dim, 0:half_dim]
						- matrix[half_dim:, half_dim:])

		coefficients = {"I": coeff1, "X": coeffX, "Y": coeffY, "Z": coeffZ}

		matrix = None

		# Recursion for the Submatrices

		for c in coefficients:
			mat = coefficients[c]
			if sparse:
				non_zero = len(mat.nonzero()[0])
			else:
				non_zero = mat.any()
			# If zero, no branching
			if non_zero != 0:
				sub_decomposition = pauli_decomposition(mat, sparse, f"{pauli_string_init}{c}", output)
				if output == "Lists":
					strings.extend(sub_decomposition[0])
					coeffs.extend(sub_decomposition[1])
				else:
					decomposition.append(sub_decomposition)

	if output == "Lists":
		return [strings, coeffs]
	else:
		output_string = "".join(decomposition)
		return output_string
