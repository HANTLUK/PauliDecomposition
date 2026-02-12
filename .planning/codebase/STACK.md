# Technology Stack

**Analysis Date:** 2026-02-12

## Languages

**Primary:**
- Python 3.13.7 - Core implementation language for all algorithms and benchmarking

## Runtime

**Environment:**
- Python 3.13.7

**Package Manager:**
- pip (standard Python package manager)
- Lockfile: Not present

## Frameworks

**Core:**
- NumPy - Numerical computing, dense matrix operations
- SciPy - Sparse matrix operations and scientific computing

**Quantum Computing Libraries:**
- Qiskit - Quantum information toolkit with SparsePauliOp for reference implementation
- PennyLane - Quantum machine learning library with pauli_decompose function
- Cirq - Google's quantum computing framework with pauli_expansion
- QuTiP - Quantum toolbox for Python, used for generating TFIM Hamiltonian

**Benchmarking & Visualization:**
- Matplotlib - Plotting and visualization of benchmark results
- timeit - Built-in Python module for timing code execution

**Testing:**
- No explicit testing framework configured (custom comparison in `TestSuite.py`)

**Build/Dev:**
- No build system detected
- No development configuration file present

## Key Dependencies

**Critical:**
- numpy - Fundamental for linear algebra and matrix operations
- scipy - Sparse matrix support for optimization on large matrices
- qiskit - Reference implementation for Pauli decomposition validation

**Algorithm Implementations (External):**
- H2ZIXY - Custom H2ZIXY algorithm import (external module)
- pauli_decomposer - Pauli Decomposer paper implementation (external module)

**Visualization & Analysis:**
- matplotlib - Generates benchmark comparison plots and data visualization

**Quantum Simulation:**
- qutip - Generates quantum operators and TFIM Hamiltonian matrices
- cirq - Alternative quantum decomposition reference
- pennylane - Alternative quantum decomposition reference

## Configuration

**Environment:**
- No explicit configuration system
- No `.env` file or configuration files detected
- All parameters hardcoded in Python scripts (e.g., `Benchmarking.py` parameters)

**Build:**
- No build configuration files present
- Direct Python script execution

## Platform Requirements

**Development:**
- Python 3.13.7
- Standard Python environment with pip package manager
- Optional: Jupyter or IPython for interactive use

**Production:**
- Python 3.13.7 runtime
- Quantum computing libraries (Qiskit, PennyLane, Cirq, QuTiP) for benchmarking
- No external services or cloud infrastructure required

## Code Organization

**Entry Points:**
- `TensorizedPauliDecomposition.py` - Main TPD algorithm implementation
- `TestSuite.py` - Validation against Qiskit reference implementation
- `Benchmarking.py` - Performance comparison of multiple algorithms
- `TFIM.py` - TFIM Hamiltonian generator for testing

**Dependencies Summary:**
- Standard library: `math`, `timeit`, `time`, `itertools`, `io`, `statistics`
- External packages: `numpy`, `scipy`, `matplotlib`, `qiskit`, `pennylane`, `cirq`, `qutip`

---

*Stack analysis: 2026-02-12*
