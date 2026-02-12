# Codebase Structure

**Analysis Date:** 2026-02-12

## Directory Layout

```
PauliDecomposition/
├── TensorizedPauliDecomposition.py  # Core algorithm implementation
├── TestSuite.py                     # Correctness validation against Qiskit
├── Benchmarking.py                  # Performance comparison harness
├── TFIM.py                          # Test data: TFIM Hamiltonian generation
├── README.md                         # Project documentation
├── LICENSE                           # Apache 2.0 license
├── .gitignore                        # Git configuration
├── .planning/                        # GSD codebase analysis output
│   └── codebase/
│       ├── ARCHITECTURE.md
│       └── STRUCTURE.md
└── .git/                             # Git repository
```

## Directory Purposes

**Root Directory:**
- Purpose: Standalone Python research implementation with no package structure
- Contains: Python scripts, documentation, license
- Key files: Core algorithm and utility modules at top level

**.planning/codebase/:**
- Purpose: GSD (Get-Shit-Done) framework analysis documents
- Generated: Yes (by codebase mapper)
- Committed: Yes
- Contents: Architecture and structure documentation for orchestrator reference

## Key File Locations

**Entry Points:**
- `TensorizedPauliDecomposition.py`: Main decomposition function; call `PauliDecomposition(matrix)`
- `TestSuite.py`: Validation script; direct execution tests TPD against Qiskit reference
- `Benchmarking.py`: Performance harness; direct execution benchmarks multiple algorithms

**Core Logic:**
- `TensorizedPauliDecomposition.py`: Lines 5-96, function `PauliDecomposition()`
  - Tensor factor extraction: lines 62-69
  - Recursive decomposition: lines 77-90
  - Base case handling: lines 45-54

**Test/Validation:**
- `TestSuite.py`: Lines 22-35
  - Matrix generation: `randomMatrix()` line 17
  - Comparison function: lines 22-33
  - Direct test execution: line 35

**Test Data Generation:**
- `TFIM.py`: Hamiltonian construction
  - Spin operators: lines 4-20
  - TFIM assembly: lines 22-35
- `Benchmarking.py`: Matrix factory functions
  - Random: line 28
  - Hermitian: lines 39-41
  - Sparse: line 32
  - One-term: lines 42-44

**Configuration/Parameters:**
- `Benchmarking.py` lines 20-24: Execution parameters
  - `stat_runs = 2`: Number of runs per test
  - `timeBarrier = 10`: Timeout in seconds
  - `stat = 1`: Enable statistics
  - `debug = 0`, `out = 1`: Output control

## Naming Conventions

**Files:**
- PascalCase for core modules: `TensorizedPauliDecomposition.py`, `TestSuite.py`, `Benchmarking.py`
- Lowercase for utility modules: `TFIM.py`

**Functions:**
- PascalCase for main exported functions: `PauliDecomposition()`, `TestSuite` test functions
- camelCase for helper/test utilities: `randomMatrix()`, `diagRandom()`, `hermRandom()`, `spin_operator()`
- Mixed convention used; prefer consistent naming

**Variables:**
- snake_case for parameters and locals: `matrix`, `sparse`, `PauliStringInit`, `output`
- camelCase for indices and intermediate values: `qBitDim`, `halfDim`, `matDim`, `nonZero`
- ALL_CAPS for constants: `stat_runs`, `timeBarrier` (convention inconsistently applied)

**Types/Data Structures:**
- Dictionary for coefficient mapping: `coefficients` dict with keys "I", "X", "Y", "Z"
- List tuples for results: `[Strings, Coeffs]` returned from PauliDecomposition
- No explicit type hints used

## Where to Add New Code

**New Algorithm Implementation:**
- Create new `.py` file at root level (same level as `TensorizedPauliDecomposition.py`)
- Export main function with signature: `def algorithm_name(matrix, sparse=False) -> [list, array]`
- Example: `NewAlgorithm.py` with `def NewDecomposition(matrix)` → returns `[pauli_strings, coefficients]`

**New Matrix Generator:**
- Add generator function to `Benchmarking.py` (lines 26-44) following pattern:
  ```python
  def newMatrixType(dim):
      # Generate and return numpy array of size (dim, dim)
      return matrix_array
  ```
- Register in `TestMatrices` dictionary (line 55)
- Add test name to `Tests` dictionary (line 54)

**New Test Case:**
- Add test function to `TestSuite.py` following pattern:
  ```python
  def testN(matrix):
      # Call algorithm
      # Return [pauli_list, coefficients]
      return [list, coeffs]
  ```
- Call comparison with appropriate method pairs (line 35 in TestSuite.py)

**Validation Function:**
- Add to `TestSuite.py` (current: `test1()`, `test2()`, `comparison()`)
- Must return `[pauli_strings_list, coefficients]` format for integration with existing comparison logic

## Special Directories

**None:** This is a flat, single-folder project with no subdirectories for source code organization.

## File Dependencies

**TensorizedPauliDecomposition.py:**
- Imports: `numpy`, `scipy.sparse`, `math`
- No internal dependencies
- Used by: TestSuite.py, Benchmarking.py

**TestSuite.py:**
- Imports: `numpy`, `math`, `TensorizedPauliDecomposition`, `qiskit.quantum_info.SparsePauliOp`
- Depends on: TensorizedPauliDecomposition.py
- External reference: Qiskit for validation

**Benchmarking.py:**
- Imports: Multiple external algorithms (H2ZIXY, pauli_decomposer, cirq, pennylane, qiskit)
- Depends on: TensorizedPauliDecomposition.py, TFIM.py
- Flexible: Can add more algorithms to `Methods` dictionary (line 51)

**TFIM.py:**
- Imports: `qutip`, `numpy`
- No dependencies on other local files
- Used by: Benchmarking.py for test data generation

## Module Interface Contracts

**PauliDecomposition(matrix, sparse=False, PauliStringInit="", output="Lists"):**
```python
# Input: Square matrix (2D array-like)
# Returns: [pauli_strings, coefficients] if output="Lists"
#          String representation if output!="Lists"
```

**Test Methods (test1, test2):**
```python
# Input: Square matrix
# Output: [pauli_list, coeffs_array]
# Pauli strings must be str() convertible for comparison
```

**Matrix Generators:**
```python
# Input: Dimension (int)
# Output: NumPy array of shape (dim, dim)
# May be complex-valued
```

---

*Structure analysis: 2026-02-12*
