from typing import Union, List
import numpy as np
import scipy.sparse as sp
import math

def pauli_decomposition(
	matrix: Union[np.ndarray, sp.spmatrix],
	sparse: bool = False,
	pauli_string_init: str = "",
	output: str = "Lists"
) -> Union[List[List], str]:
	"""Decompose a matrix into a sum of Pauli operator tensor products.

	Uses a recursive tensor factorization approach: at each recursion level,
	the matrix is split into four submatrices corresponding to the Pauli
	basis {I, X, Y, Z}, and the algorithm recurses on each non-zero
	submatrix to build up the full Pauli string decomposition.

	Non-power-of-2 matrices are zero-padded to the next power of 2.

	Parameters
	----------
	matrix : np.ndarray or scipy.sparse.spmatrix
		Square matrix to decompose. Can be dense (NumPy array) or sparse
		(SciPy sparse matrix). Non-power-of-2 dimensions are automatically
		padded with zeros.
	sparse : bool, optional
		Whether ``matrix`` is in SciPy sparse format. Default is False.
	pauli_string_init : str, optional
		Prefix for Pauli strings during recursion. Used internally;
		callers should leave this as the default empty string.
	output : str, optional
		Output format. ``"Lists"`` (default) returns a list of two lists
		``[pauli_strings, coefficients]``. Any other value returns a
		formatted string representation.

	Returns
	-------
	list of [list of str, list of complex] or str
		If ``output == "Lists"``: returns ``[pauli_strings, coefficients]``
		where ``pauli_strings`` is a list of Pauli operator strings
		(e.g., ``"IXYZ"``) and ``coefficients`` is a list of complex
		coefficients.
		If ``output != "Lists"``: returns a single formatted string with
		all terms.

	Examples
	--------
	>>> import numpy as np
	>>> from TensorizedPauliDecomposition import pauli_decomposition
	>>> matrix = np.array([[1, 0], [0, -1]])  # Pauli Z matrix
	>>> strings, coeffs = pauli_decomposition(matrix)
	>>> strings
	['Z']
	>>> coeffs
	[1.0]
	"""

	mat_dim = matrix.shape[0]
	# Determine the number of qubits: n = ceil(log2(dim))
	# A 2^n x 2^n matrix decomposes into n-qubit Pauli strings
	qubit_dim = math.ceil(np.log(mat_dim)/np.log(2))

	# Zero-pad the matrix to the next power of 2 if needed.
	# This ensures the matrix dimensions match 2^n for n-qubit decomposition.

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


	# Base case: 1x1 matrix (scalar). The single element is the coefficient
	# for the accumulated Pauli string. Only record non-zero terms.
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

	# Tensor factorization using the Pauli basis.
	# For a 2^n x 2^n matrix M, split into 2^(n-1) x 2^(n-1) blocks:
	#   M = [[A, B],    where A = M[0:h, 0:h], B = M[0:h, h:2h],
	#        [C, D]]          C = M[h:2h, 0:h], D = M[h:2h, h:2h]
	#
	# The Pauli coefficients for the leading qubit are:
	#   coeff_I = (A + D) / 2     (identity component)
	#   coeff_X = (C + B) / 2     (Pauli X component)
	#   coeff_Y = -i(C - B) / 2   (Pauli Y component)
	#   coeff_Z = (A - D) / 2     (Pauli Z component)
	#
	# Each coefficient matrix is itself a 2^(n-1) x 2^(n-1) matrix
	# that will be recursively decomposed for the remaining qubits.
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

		# Release reference to the original matrix to reduce memory usage
		# during deep recursion on large matrices.
		matrix = None

		# Recurse on each non-zero Pauli coefficient matrix.
		# Append the current Pauli label (I/X/Y/Z) to the growing string.
		# Skip zero matrices to avoid unnecessary branches (sparsity optimization).
		for c in coefficients:
			mat = coefficients[c]
			if sparse:
				non_zero = len(mat.nonzero()[0])
			else:
				non_zero = mat.any()
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
