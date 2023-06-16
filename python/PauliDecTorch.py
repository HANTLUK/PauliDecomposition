import numpy as np
import scipy.sparse as sp
import itertools
import torch as tch

debug = 0

def PauliDecTorch(matrix, PauliStringInit = ""):
	"""
	Implementation using Torch

	"""
	mat1 = tch.tensor([[1.,0.],[0.,1.]],dtype=tch.cdouble)
	matX = tch.tensor([[0.,1.],[1.,0.]],dtype=tch.cdouble)
	matY = tch.tensor([[0,-1.j],[1.j,0]],dtype=tch.cdouble)
	matZ = tch.tensor([[1.,0.],[0.,-1.]],dtype=tch.cdouble)
	Paulis = [["1", mat1], ["X", matX], ["Y", matY], ["Z", matZ]]
	for n,Pauli in Paulis:
		Pauli.conj()
# Initialize values
	matrix = tch.tensor(matrix)
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
			matrixN = tch.reshape(matrix,[d2,2,d2,2])
			matrix = tch.transpose(matrixN,dim0=1,dim1=2)
# Partial trace gives rest or component with respect to this Pauli.
			mult = tch.multiply(matrix,tch.transpose(PauliMatrix.resolve_conj(),dim0=0,dim1=1))
			mult = tch.transpose(mult,dim0=0,dim1=2)
			mult = tch.transpose(mult,dim0=0,dim1=1)
			mult = tch.transpose(mult,dim0=0,dim1=3)
			rest = 0.5*tch.sum(mult,dim=(0,1))
# Ignore trivial parts of decomposition
			if tch.any(rest):
# Recursively Reduce Dimension
				PauliString += Pauli
				decomposition += PauliDecTorch(rest,PauliString)
# In 2 dimensions
		elif log2dim == 1:
			mult = tch.matmul(matrix,tch.transpose(PauliMatrix.resolve_conj(),dim0=0,dim1=1))
			rest = 0.5*tch.sum(mult,dim=(0,1))
# Ignore trivial parts of decomposition
			if tch.any(rest):
				PauliString += Pauli + (", "+str(rest))
				decomposition.append(PauliString)
	return decomposition
