import numpy as np
import scipy.sparse as sp
import itertools
import tensorflow as tf

debug = 0

def PauliDecTensorFlow(matrix, PauliStringInit = ""):
	"""
	Implementation using TensorFlow

	"""
	mat1 = tf.convert_to_tensor(np.array([[1.,0.],[0.,1.]],dtype=np.cdouble))
	matX = tf.convert_to_tensor(np.array([[0.,1.],[1.,0.]],dtype=np.cdouble))
	matY = tf.convert_to_tensor(np.array([[0,-1.j],[1.j,0]],dtype=np.cdouble))
	matZ = tf.convert_to_tensor(np.array([[1.,0.],[0.,-1.]],dtype=np.cdouble))
	Paulis = [["1", mat1], ["X", matX], ["Y", matY], ["Z", matZ]]
# Initialize values
	matrix = tf.convert_to_tensor(matrix)
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
			matrixN = tf.reshape(matrix,[d2,2,d2,2])
			matrix = tf.transpose(matrixN,perm=[0,2,1,3])
# Partial trace gives rest or component with respect to this Pauli.
			mult = tf.matmul(matrix,tf.transpose(PauliMatrix,perm=[0,1],conjugate=True))
			mult = tf.transpose(mult,perm=[2,3,1,0])
			rest = 0.5*tf.reduce_sum(mult,axis = [0,1])
# Ignore trivial parts of decomposition
			if tf.math.count_nonzero(rest) != 0:
# Recursively Reduce Dimension
				PauliString += Pauli
				decomposition += PauliDecTensorFlow(rest,PauliString)
# In 2 dimensions Calculate Trace
		elif log2dim == 1:
			mult = tf.matmul(matrix,tf.transpose(PauliMatrix,perm=[0,1],conjugate=True))
			rest = 0.5*tf.reduce_sum(mult,axis=[0,1])
# Ignore trivial parts of decomposition
			if tf.math.count_nonzero(rest) != 0:
				PauliString += Pauli + (", "+str(rest))
				decomposition.append(PauliString)
	return decomposition
