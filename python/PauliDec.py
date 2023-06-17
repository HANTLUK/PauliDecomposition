import numpy as np
import scipy.sparse as sp
import itertools

debug = 0

"""
Input a 2**n by 2**n matrix and return array of Pauli strings.
Naive approach: 4**d matrices with one 2**d*2**d multipliication.
New approach: maximal 4**d depth with each one scalar multiplication and matrix addition.
Simplification, if some (Early) Paulis do not appear (Symmetry of the Matrix).
"""

def PauliDec(matrix, PauliStringInit = ""):
	"""
	Returns the Pauli Decomposition of a Matrix recursively.
	Input matrix: Matrix to decompose.
	PauliStringInit: begin of the Pauli String.
	PreferredFactor: In which indices are expected symmetries.
	Output: If 2x2, PauliString with prefactor
			If Larger, Recursively PauliDec of PartialTraces
	"""
	mat1 = np.array([[1.,0.],[0.,1.]],dtype=np.cdouble)
	matX = np.array([[0.,1.],[1.,0.]],dtype=np.cdouble)
	matY = np.array([[0,-1.j],[1.j,0]],dtype=np.cdouble)
	matZ = np.array([[1.,0.],[0.,-1.]],dtype=np.cdouble)
	Paulis = [["1", mat1], ["X", matX], ["Y", matY], ["Z", matZ]]
# Initialize values
	if debug: print("Matrix ",matrix)
	if debug: print("Shape ",matrix.shape)
	dim = matrix.shape[0]
	log2dim = int(np.log(dim)/np.log(2))
	decomposition = []
# Iterate over Possible Pauli Strings
	for Pauli,PauliMatrix in Paulis:
		PauliString = PauliStringInit
# Submatrices for higher dimension
		if log2dim > 1:
			d2 = int(dim/2)
# Blockmatrix decomposition
			matrixN = matrix.reshape(d2,2,d2,2).swapaxes(1,2)
# Partial trace gives rest or component with respect to this Pauli.
			mult = np.multiply(matrixN,np.conjugate(np.transpose(PauliMatrix)))
			mult = mult.swapaxes(1,3).swapaxes(0,2)
			rest = 1./2.*np.sum(mult,axis = (0,1))
# Ignore trivial parts of decomposition
			if rest.any():
# Recursively Reduce Dimension
				PauliString += Pauli
				decomposition += PauliDec(rest,PauliString)
# In 2 dimensions
		elif log2dim == 1:
			mult = np.matmul(matrix,np.conjugate(np.transpose(PauliMatrix)))
			rest = 1./2.*np.trace(mult)
# Ignore trivial parts of decomposition
			if rest.any():
				PauliString += Pauli + (", "+str(rest))
				decomposition.append(PauliString)
	return decomposition
