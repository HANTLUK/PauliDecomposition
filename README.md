# Tensorized Pauli Decomposition Algorithm

This repository contains a Python implementation of the algorithm described in the paper: "[Tensorized Pauli decomposition algorithm](https://doi.org/10.48550/arXiv.2310.13421)".. A preprint of this paper is currently on the arXiv. Please cite this paper as:

Hantzko, L., Binkowski, L., Gupta, S. (2023). Tensorized Pauli decomposition algorithm, arXiv:2310.13421 [quant-ph]

The corresponding BibTex entry is:

@misc{Hantzko2023,  
&nbsp;&nbsp; author={Hantzko, Lukas and Binkowski, Lennart and Gupta, Sabhyata},  
&nbsp;&nbsp; year={2023},  
&nbsp;&nbsp; title={{Tensorized Pauli decomposition algorithm}},  
&nbsp;&nbsp; eprint={2310.13421},  
&nbsp;&nbsp; archivePrefix={arXiv},  
&nbsp;&nbsp; primaryClass={quanth-ph}  
}

## TensorizedPauliDecomposition
This file contains the actual TPD algorithm.
The TPD inputs a square matrix (numpy array or scipysparse) and outputs its Pauli decomposition.
The default implementation is working with nonsparse matrices.
Sparsity can be exploited by setting the optional argument sparse to True.
## TestSuite
The test suite compares the result of different Pauli decomposition implementations to verify their correctness.
As a point of reference Qiskit's SparsePauliOp method is used.
It can also be used for other algorithms then presented, if the output is in the right format including a list of Pauli Strings and a list/np.array of the coefficients.
