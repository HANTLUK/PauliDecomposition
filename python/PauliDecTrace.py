import numpy as np
import scipy.sparse as sp
import itertools

debug = 0

def PauliDecTrace(matrix, PauliStringInit = "", MatInit = np.array([1])):

	mat1 = np.array([[1.,0.],[0.,1.]],dtype=np.cdouble)
	matX = np.array([[0.,1.],[1.,0.]],dtype=np.cdouble)
	matY = np.array([[0,-1.j],[1.j,0]],dtype=np.cdouble)
	matZ = np.array([[1.,0.],[0.,-1.]],dtype=np.cdouble)
	Paulis = [["1", mat1], ["X", matX], ["Y", matY], ["Z", matZ]]

	dim = matrix.shape[0]
	log2dim = int(np.log(dim)/np.log(2))
	iter = MatInit.shape[0]
	decomposition = []
	PauliString = PauliStringInit
	if iter >= dim:
		prod = np.matmul(matrix,np.conjugate(np.transpose(MatInit)))
		coeff = 1./(2.**(dim/2.))*np.trace(prod)
		if coeff != 0:
			PauliString += ", "+str(coeff)
			decomposition.append(PauliString)
		return decomposition
	else:
		for Pauli,PauliMatrix in Paulis:
			if iter > 1:
				MatInit.reshape(int(iter/2),2,int(iter/2),2).swapaxes(1,2)
			matNew = np.tensordot(PauliMatrix,MatInit,0).swapaxes(1,2).reshape(2*iter,2*iter)
			PauliString += Pauli
			recursion = PauliDecTrace(matrix,PauliString,matNew)
			if recursion != []:
				decomposition += recursion
			PauliString = PauliStringInit

	return decomposition
