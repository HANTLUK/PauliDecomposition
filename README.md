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

## TensorizedPauliDecomposition
This file contains the actual TPD algorithm.
The TPD inputs a square matrix (numpy array or scipysparse) and outputs its Pauli decomposition.
The default implementation is working with nonsparse matrices.
Sparsity can be exploited by setting the optional argument sparse to True.
## TestSuite
The test suite compares the result of different Pauli decomposition implementations to verify their correctness.
As a point of reference Qiskit's SparsePauliOp method is used.
It can also be used for other algorithms then presented, if the output is in the right format including a list of Pauli Strings and a list/np.array of the coefficients.
## Benchmarking
This File does the Benchmarking and outputs tables of runtimes. To run, you need to import the suitable libraries and implementations of the algorithms you want to compare. We included test matrices and tfim Hamiltonian as a seperate file.
