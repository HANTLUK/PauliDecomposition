import numpy as np
import scipy.sparse as sp
import itertools

debug = 0

def PauliDecPaper(matrix):

	mat1 = np.array([[1.,0.],[0.,1.]],dtype=np.cdouble)
	matX = np.array([[0.,1.],[1.,0.]],dtype=np.cdouble)
	matY = np.array([[0,-1.j],[1.j,0]],dtype=np.cdouble)
	matZ = np.array([[1.,0.],[0.,-1.]],dtype=np.cdouble)

	eps = 1.e-5

	dim = matrix.shape[0]

	Paulis = {"1":mat1,"X":matX,"Y":matY,"Z":matZ}

	NumTensorRepetitions = int(np.log(dim)/np.log(2))
	NumTotalTensors = 4**NumTensorRepetitions
	PauliKeyList = []
	KeysToDelete = []
	PauliDict = {}
	def PauliDictValues(l):
		yield from itertools. product(*([l] *NumTensorRepetitions))
	for x in PauliDictValues("1XYZ"):
		PauliKeyList. append ("".join(x))
	for y in PauliKeyList:
		PauliDict[y] = 0
	for key in PauliDict:
		TempList = []
		PauliTensors = []
		TempKey = str(key)
		for string in TempKey:
			TempList.append(string)
		for SpinMatrix in TempList:
			PauliTensors.append(Paulis[SpinMatrix])
		PauliDict[key] = PauliTensors
		CurrentMatrix = PauliDict[key].copy()
		# Compute Tensor Product between I, X, Y, Z matrices
		for k in range (1, NumTensorRepetitions ):
			TemporaryDict = np.kron(CurrentMatrix[k -1],CurrentMatrix[k])
			CurrentMatrix[k] = TemporaryDict
		PauliDict[key] = CurrentMatrix[-1]

	VecHamElements = np.zeros(int(dim**2),dtype=np.cdouble)
	h = 0
	for i in range (0,dim):
		for j in range (0,dim):
			arr = []
			VecHamElements[h] = matrix[i,j]
			for key in PauliDict:
				TempVar = PauliDict[key]
				arr.append(TempVar[i,j])
			if i == 0 and j == 0:
				FinalMat = np.array(arr.copy())
			else :
				FinalMat = np.vstack((FinalMat,arr))
			h += 1
	x = np.linalg.solve(FinalMat,VecHamElements)
	decomposition = []
	var_list = list(PauliDict.keys())

	for i in range(len(PauliDict)):
		b = x[i]
		if abs(b)>eps:
			decomposition.append(str(var_list[i])+", "+str(b))
	return decomposition
