import qutip as qt
import numpy as np
from typing import List, Tuple

def spin_operator(N: int) -> Tuple[List, List]:
	"""Construct N-qubit spin operator lists for the transverse field Ising model.

	Builds lists of N-body tensor products of Pauli sigma_x and sigma_z
	operators, where each list element has the operator acting on one
	specific qubit site and identity on all others.

	Parameters
	----------
	N : int
	    Number of qubit sites (spins) in the chain.

	Returns
	-------
	tuple of (list, list)
	    ``(sx_list, sz_list)`` where each list has N elements.
	    ``sx_list[n]`` is the sigma_x operator acting on site n
	    (tensor product with identity on all other sites).
	    ``sz_list[n]`` is the sigma_z operator acting on site n.

	Examples
	--------
	>>> sx_list, sz_list = spin_operator(2)
	>>> len(sx_list)
	2
	"""
	# Single-site Pauli operators (2x2 matrices)
	si = qt.qeye(2)    # Identity
	sx = qt.sigmax()    # Pauli X (sigma_x)
	sz = qt.sigmaz()    # Pauli Z (sigma_z)

	sx_list = []
	sz_list = []

	# Build N-body operators: place sigma on site n, identity elsewhere.
	# op_list starts as [I, I, ..., I], then site n is replaced.
	for n in range(N):
		op_list = []
		for m in range(N):
			op_list.append(si)
		op_list[n] = sz
		sz_list.append(qt.tensor(op_list))
		op_list[n] = sx
		sx_list.append(qt.tensor(op_list))
	return sx_list, sz_list

def tfim_hamiltonian(dim: int) -> np.ndarray:
	"""Generate the transverse field Ising model Hamiltonian matrix.

	Constructs H = h_x * sum_n(sigma_x_n) + J_zz * sum_n(sigma_z_n * sigma_z_{n+1})
	for a 1D chain with open boundary conditions.

	Parameters
	----------
	dim : int
	    Matrix dimension (must be a power of 2). The number of qubits
	    is inferred as N = log2(dim).

	Returns
	-------
	np.ndarray
	    The full dense Hamiltonian matrix of shape (dim, dim).

	Examples
	--------
	>>> H = tfim_hamiltonian(4)  # 2-qubit TFIM
	>>> H.shape
	(4, 4)
	"""
	N = int(np.log(dim)/np.log(2))
	# Coupling constants for the TFIM
	j_zz = -0.5     # Ising interaction strength (nearest-neighbor ZZ coupling)
	h_x = -0.05     # Transverse field strength (external X field)
	sx_list, sz_list = spin_operator(N)
	j_z_array = j_zz*np.ones(N)
	h_x_array = h_x*np.ones(N)

	hamiltonian = 0
	# Transverse field terms: h_x * sigma_x on each site
	for n in range(N):
		hamiltonian += h_x_array[n] * sx_list[n]
	# Ising interaction terms: J_zz * sigma_z_n * sigma_z_{n+1} (nearest-neighbor)
	for n in range(N - 1):
		hamiltonian += j_z_array[n] * sz_list[n] * sz_list[n + 1]
	return hamiltonian.full()
