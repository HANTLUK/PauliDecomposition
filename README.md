# Tensorized Pauli Decomposition Algorithm

This repository contains a Python implementation of the algorithm described in the paper: "[Tensorized Pauli decomposition algorithm](https://iopscience.iop.org/article/10.1088/1402-4896/ad6499)", as published in [Physica Scripta](https://iopscience.iop.org/journal/1402-4896). The paper is also available on the [arXiv](https://doi.org/10.48550/arXiv.2310.13421). Please cite this paper as:

Lukas Hantzko *et al* 2024 *Phys. Scr.* **99** 085128

The corresponding BibTex entry is:

@article{Hantzko2024TensorizedPauliDecompositionAlgorithm,
&nbsp;&nbsp; author={Hantzko, Lukas and Binkowski, Lennart and Gupta, Sabhyata},
&nbsp;&nbsp; year={2024},
&nbsp;&nbsp; title={Tensorized Pauli decomposition algorithm},
&nbsp;&nbsp; journal={Phys. Scr.},
&nbsp;&nbsp; volume={99},
&nbsp;&nbsp; number={8},
&nbsp;&nbsp; pages={085128},
&nbsp;&nbsp; publisher={IOP Publishing},
&nbsp;&nbsp; doi={10.1088/1402-4896/ad6499},
&nbsp;&nbsp; url={ht<span>tps://</span>dx.doi.org/10.1088/1402-4896/ad6499}
}

## Installation

**Python Version:** Python 3.7 or higher

**Core Dependencies:**
```bash
pip install numpy scipy
```

**Optional Dependencies:**

For testing and comparison with Qiskit (TestSuite.py):
```bash
pip install qiskit
```

For TFIM Hamiltonian generation (TFIM.py):
```bash
pip install qutip
```

For benchmarking against other decomposition methods (Benchmarking.py):
```bash
pip install qiskit pennylane cirq
# Also requires h2zixy and pauli_decomposer packages
```

**Note:** This project is used by importing modules directly - no pip installation of the package itself is required.

## Usage

### Basic decomposition (dense matrix)

```python
import numpy as np
from TensorizedPauliDecomposition import pauli_decomposition

# Decompose a Pauli Z matrix
Z = np.array([[1, 0], [0, -1]])
pauli_strings, coefficients = pauli_decomposition(Z)
print(pauli_strings)   # ['Z']
print(coefficients)     # [1.0]
```

### Multi-qubit matrix

```python
# Decompose a 4x4 matrix (2-qubit system)
matrix = np.random.rand(4, 4) + 1j * np.random.rand(4, 4)
pauli_strings, coefficients = pauli_decomposition(matrix)
for s, c in zip(pauli_strings, coefficients):
    print(f"{c:.4f} * {s}")
```

### Sparse matrix input

```python
import scipy.sparse as sp

sparse_matrix = sp.random(8, 8, density=0.1, format="csr")
pauli_strings, coefficients = pauli_decomposition(sparse_matrix, sparse=True)
```

### String output format

```python
result = pauli_decomposition(Z, output="String")
print(result)  # formatted string representation
```

### Non-power-of-2 matrices

```python
# 3x3 matrix is automatically zero-padded to 4x4
matrix_3x3 = np.random.rand(3, 3)
pauli_strings, coefficients = pauli_decomposition(matrix_3x3)
```

## API Reference

### TensorizedPauliDecomposition

**`pauli_decomposition(matrix, sparse=False, pauli_string_init="", output="Lists")`**

Decompose a matrix into a sum of Pauli operator tensor products.

- **Parameters:**
  - `matrix` (np.ndarray or scipy.sparse.spmatrix): Square matrix to decompose. Non-power-of-2 dimensions are automatically zero-padded.
  - `sparse` (bool, optional): Whether the matrix is in SciPy sparse format. Default is False.
  - `pauli_string_init` (str, optional): Prefix for Pauli strings during recursion. For internal use; callers should leave this as the default empty string.
  - `output` (str, optional): Output format. "Lists" (default) returns `[pauli_strings, coefficients]`. Any other value returns a formatted string representation.

- **Returns:** `[list of str, list of complex]` if `output="Lists"`, otherwise `str`

### TestSuite

**`decompose_with_qiskit(matrix)`**

Decompose a matrix using Qiskit's SparsePauliOp for reference comparison.

- **Parameters:**
  - `matrix` (np.ndarray): Square matrix to decompose.

- **Returns:** `[PauliList, np.ndarray]` - Pauli strings and coefficients from Qiskit's decomposition.

**`decompose_with_tpd(matrix)`**

Decompose a matrix using the tensorized Pauli decomposition algorithm.

- **Parameters:**
  - `matrix` (np.ndarray): Square matrix to decompose.

- **Returns:** `[list of str, list of complex]` - Pauli strings and coefficients from the TPD algorithm.

**`random_matrix(dim)`**

Generate a random complex matrix of given dimension.

- **Parameters:**
  - `dim` (int): Side length of the square matrix.

- **Returns:** `np.ndarray` - Random complex matrix of shape (dim, dim).

**`compare_methods(method1, method2, matrix)`**

Compare two Pauli decomposition methods for equivalence.

- **Parameters:**
  - `method1` (callable): First decomposition function returning `[pauli_strings, coefficients]`.
  - `method2` (callable): Second decomposition function returning `[pauli_strings, coefficients]`.
  - `matrix` (np.ndarray): Square matrix to decompose with both methods.

- **Returns:** `bool` - True if both methods produce the same Pauli strings and coefficients within tolerance (1e-5), False otherwise.

### TFIM

**`spin_operator(N)`**

Construct N-qubit spin operator lists for the transverse field Ising model.

- **Parameters:**
  - `N` (int): Number of qubit sites (spins) in the chain.

- **Returns:** `(list, list)` - `(sx_list, sz_list)` where each list has N elements. `sx_list[n]` is the sigma_x operator acting on site n, and `sz_list[n]` is the sigma_z operator acting on site n.

**`tfim_hamiltonian(dim)`**

Generate the transverse field Ising model Hamiltonian matrix.

- **Parameters:**
  - `dim` (int): Matrix dimension (must be a power of 2). The number of qubits is inferred as N = log2(dim).

- **Returns:** `np.ndarray` - The full dense Hamiltonian matrix of shape (dim, dim).

### Benchmarking

**`diag_random(dim)`**

Generate a random complex diagonal matrix.

- **Parameters:**
  - `dim` (int): Side length of the square matrix.

- **Returns:** `np.ndarray` - Complex diagonal matrix of shape (dim, dim).

**`random_matrix(dim)`**

Generate a random complex matrix.

- **Parameters:**
  - `dim` (int): Side length of the square matrix.

- **Returns:** `np.ndarray` - Random complex matrix of shape (dim, dim).

**`identity_matrix(dim)`**

Generate an identity matrix.

- **Parameters:**
  - `dim` (int): Side length of the square matrix.

- **Returns:** `np.ndarray` - Identity matrix of shape (dim, dim).

**`sparse_random(dim)`**

Generate a random sparse matrix in CSR format with density 1/dim.

- **Parameters:**
  - `dim` (int): Side length of the square matrix.

- **Returns:** `scipy.sparse.csr_matrix` - Random sparse matrix of shape (dim, dim).

**`pauli_dec_sparse(matrix)`**

Run Pauli decomposition on a sparse matrix.

- **Parameters:**
  - `matrix` (scipy.sparse.spmatrix): Sparse matrix to decompose.

- **Returns:** `list` - Pauli decomposition result from `pauli_decomposition` with `sparse=True`.

**`symm_random(dim)`**

Generate a random complex symmetric matrix (M + M^T).

- **Parameters:**
  - `dim` (int): Side length of the square matrix.

- **Returns:** `np.ndarray` - Symmetric complex matrix of shape (dim, dim).

**`herm_random(dim)`**

Generate a random Hermitian matrix (M + M^dagger).

- **Parameters:**
  - `dim` (int): Side length of the square matrix.

- **Returns:** `np.ndarray` - Hermitian matrix of shape (dim, dim).

**`one_term(dim)`**

Generate a matrix with a single tensor-product term using Kronecker product structure.

- **Parameters:**
  - `dim` (int): Side length of the square matrix. Must be even.

- **Returns:** `np.ndarray` - Matrix of shape (dim, dim) with structure kron(random_2x2, I_{dim/2}).

## TensorizedPauliDecomposition

This module contains the core TPD algorithm implementation. The algorithm decomposes a square matrix (NumPy array or SciPy sparse matrix) into a sum of Pauli operator tensor products. The default implementation works with dense matrices, but sparsity can be exploited by setting the optional argument `sparse=True`.

## TestSuite

The test suite compares the results of different Pauli decomposition implementations to verify their correctness. Qiskit's SparsePauliOp method is used as a reference implementation. The suite can be adapted for other decomposition algorithms as long as they output a list of Pauli strings and a list/array of coefficients in the correct format.

## TFIM

This module provides utilities for generating transverse field Ising model (TFIM) Hamiltonians, which are commonly used as test cases for Pauli decomposition algorithms.

## Benchmarking

This module performs runtime benchmarking and outputs tables comparing different decomposition algorithms. To run benchmarks, you need to import the appropriate libraries and algorithm implementations you want to compare. Test matrix generators and TFIM Hamiltonian generation are included.
