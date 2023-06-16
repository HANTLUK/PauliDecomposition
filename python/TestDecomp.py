import numpy as np
import timeit
import scipy.sparse as sp
import itertools
import matplotlib.pyplot as plt
from PauliDec import PauliDec
from PauliDecTrace import PauliDecTrace
from PauliDecLinA import PauliDecLinA

out = 1
test = 0
runs = 1
speed = 1
diag = 1
rand = 1

CompareMethods = ["Tensor Product", "Trace", "Linear Algebra"]

Methods = {"Tensor Product": PauliDec, "Trace": PauliDecTrace, "Linear Algebra": PauliDecLinA}
MaxSizes = {"Tensor Product": 10, "Trace": 8, "Linear Algebra": 6}
Results = {}
ResultsOne = {}

# Test of Speed for Random Matrices or unit matrix
if speed:
	if out: print("Speed Test \n")
	for Method in CompareMethods:
		if out: print(Method+":")
		tab = []
		tabOne = []
		for n in range(1,MaxSizes[Method]):
			dim = 2**n
			if rand:
				start_time = timeit.default_timer()
				for i in range(runs):
					Methods[Method](np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim)))
				elapsed = timeit.default_timer() - start_time
				tab.append(elapsed)
				if out: print("dim",n,": ",elapsed)
			if diag:
				start_time = timeit.default_timer()
				for i in range(runs):
					Methods[Method](np.identity(dim))
				elapsed = timeit.default_timer() - start_time
				tabOne.append(elapsed)
				if out: print("dim",n,": ",elapsed)
		Results[Method] = tab
		ResultsOne[Method] = tabOne

	if rand:
		fig,ax = plt.subplots(figsize=(5,5),dpi=150)
		plt.xlabel('Number of Qubits')
		plt.ylabel('Computation Time (s)')
		plt.title('Comparison of Computation Time (Random Matrix)')
		plt.grid(True)
		for Method in CompareMethods:
			ax.plot(range(1,MaxSizes[Method]),np.log(Results[Method])/np.log(4), 'o-', label=Method)
		tab = [0.000000130000000, 0.000000060000000, 0.000000260000000, 0.000001140000000, 0.000005070000000, 0.000022110000000, 0.000094000000000, 0.000399590000000, 0.001710040000000, 0.007222440000000, 0.030391740000000, 0.126972590000000]
		ax.plot(range(1,13),np.log(tab)/np.log(4), 'o-', label="Tensor Product (c++)")
		plt.legend()
		fig.savefig("plot.png",dpi=150)

	if diag:
		fig,ax = plt.subplots(figsize=(5,5),dpi=150)
		plt.xlabel('Number of Qubits')
		plt.ylabel('Computation Time (s)')
		plt.title('Comparison of Computation Time (Unit Matrix)')
		plt.grid(True)
		for Method in CompareMethods:
			ax.plot(range(1,MaxSizes[Method]),np.log(ResultsOne[Method])/np.log(4), 'o-', label=Method)
		fig.savefig("plot2.png",dpi=150)

runs = 1
test = 0
out = 1
acc = 0
CompareMethods = []

# Tests of Correct Computation
if acc:
	if out: print("Test of Correctness")
	testMat1 = np.array([[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,-1]],dtype=np.cdouble)
	testMat2 = np.array([[-1,0],[0,1]],dtype=np.cdouble)

	for Method in CompareMethods:
		if test: print(Method)
		decomposition = Methods[Method](testMat1)
		if out: print(Method+":")
		for n in decomposition:
			if out: print(n)

	for i in range(runs):
		rand = np.add(np.random.rand(4,4),1.j*np.random.rand(4,4))
		for Method in CompareMethods:
			decomposition = Methods[Method](rand)
			if out: print(Method+":")
			for n in decomposition:
				if out: print(n)
