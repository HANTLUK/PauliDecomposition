import qutip as qt
import numpy as np

def spin_operator(N):
	si = qt.qeye(2)
	sx = qt.sigmax()
	sz = qt.sigmaz()

	sx_list = []
	sz_list = []

	for n in range(N):
		op_list = []
		for m in range(N):
			op_list.append(si)
		op_list[n] = sz
		sz_list.append(qt.tensor(op_list))
		op_list[n] = sx
		sx_list.append(qt.tensor(op_list))
	return sx_list, sz_list

def tfimHamiltonian(dim):
	N = int(np.log(dim)/np.log(2))
	Jzz = -0.5
	hx = -0.05
	sx_list, sz_list = spin_operator(N)
	Jzs = Jzz*np.ones(N)
	hxs = hx*np.ones(N)

	H = 0
	for n in range(N):
		H += hxs[n] * sx_list[n]
	for n in range(N - 1):
		H += Jzs[n] * sz_list[n] * sz_list[n + 1]
	return H.full()
