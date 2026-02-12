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

def tfim_hamiltonian(dim):
	N = int(np.log(dim)/np.log(2))
	j_zz = -0.5
	h_x = -0.05
	sx_list, sz_list = spin_operator(N)
	j_z_array = j_zz*np.ones(N)
	h_x_array = h_x*np.ones(N)

	hamiltonian = 0
	for n in range(N):
		hamiltonian += h_x_array[n] * sx_list[n]
	for n in range(N - 1):
		hamiltonian += j_z_array[n] * sz_list[n] * sz_list[n + 1]
	return hamiltonian.full()
