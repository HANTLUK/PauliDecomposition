# Architecture

**Analysis Date:** 2026-02-12

## Pattern Overview

**Overall:** Decomposition Algorithm with Test Harness and Benchmarking Framework

**Key Characteristics:**
- Single-purpose core algorithm focused on Pauli decomposition
- Modular test and benchmarking infrastructure
- Recursive tensor product factorization approach
- Support for both dense and sparse matrix formats
- External algorithm comparison framework

## Layers

**Algorithm Layer:**
- Purpose: Implements the tensorized Pauli decomposition algorithm core
- Location: `TensorizedPauliDecomposition.py`
- Contains: Main decomposition function with recursive tensor factorization logic
- Depends on: NumPy, SciPy sparse utilities, Python math library
- Used by: TestSuite, Benchmarking

**Test & Validation Layer:**
- Purpose: Verifies correctness of decomposition implementations against reference implementations
- Location: `TestSuite.py`
- Contains: Comparison logic, test matrix generation, validation functions
- Depends on: TensorizedPauliDecomposition, Qiskit SparsePauliOp reference
- Used by: Manual test execution

**Benchmarking & Analysis Layer:**
- Purpose: Measures runtime performance across different algorithms and matrix types
- Location: `Benchmarking.py`
- Contains: Performance testing harness, multiple algorithm integrations, result collection
- Depends on: TensorizedPauliDecomposition, TFIM, external algorithm libraries
- Used by: Performance analysis scripts

**Test Data Generation Layer:**
- Purpose: Generates test matrices and quantum system representations
- Location: `TFIM.py`, matrix generators in Benchmarking and TestSuite
- Contains: Random matrix generators, TFIM Hamiltonian construction, spin operators
- Depends on: NumPy, QuTiP for quantum operators
- Used by: TestSuite, Benchmarking

## Data Flow

**Decomposition Process:**

1. Input: Square matrix (NumPy array or SciPy sparse format) → `PauliDecomposition()`
2. Dimension analysis: Calculate qubit dimension from matrix size
3. Padding: Extend to power-of-2 dimension if needed
4. Tensor coefficient extraction: Calculate I, X, Y, Z coefficients from matrix slices
5. Recursive branching: For each non-zero coefficient, recursively decompose the coefficient matrix
6. Base case: Return Pauli string and coefficient when dimension = 1
7. Output: Two lists - Pauli strings and their coefficients (or formatted string)

**Testing Process:**

1. Generate test matrix (random, diagonal, TFIM, etc.)
2. Apply two methods: TPD algorithm and Qiskit reference
3. Compare Pauli strings (as strings) and coefficients (within epsilon tolerance)
4. Return boolean result (True = equivalent)

**Benchmarking Process:**

1. Select test type and algorithm(s) to compare
2. For each qubit dimension (2 to max):
   - Generate test matrix of size 2^n × 2^n
   - Run algorithm `stat_runs` times
   - Record elapsed time for each run
   - Calculate mean runtime
   - Stop if mean exceeds `timeBarrier`
3. Write results to `.dat` files
4. Optional statistical analysis

**State Management:**
- No persistent state; all computations are functional transformations
- Matrix dimensions determine qubit bit width
- Coefficient matrices are intermediate results during recursion
- Results are returned as immutable lists/arrays

## Key Abstractions

**PauliDecomposition Function:**
- Purpose: Decomposes a matrix into sum of Pauli operator terms
- Location: `TensorizedPauliDecomposition.py` lines 5-96
- Pattern: Recursive tensor product factorization
- Input contract: Square matrix (2D array-like), optional sparse flag
- Output contract: [Pauli strings list, coefficients list] or string representation

**Matrix Generator Functions:**
- Purpose: Create matrices with specific properties for testing
- Examples: `randomMatrix()` (lines 28-29 in Benchmarking.py), `hermRandom()` (lines 39-41), `diagRandom()` (lines 26-27), `tfimHamiltonian()` (TFIM.py lines 22-35)
- Pattern: Parameterized factory functions returning NumPy arrays
- Usage: Test case generation with controlled matrix characteristics

**Spin Operator Construction:**
- Purpose: Build quantum spin operators for TFIM Hamiltonian
- Location: `TFIM.py` lines 4-20
- Pattern: Tensor products of single-qubit operators
- Key insight: Builds Pauli-X and Pauli-Z operators for N-qubit systems

## Entry Points

**Direct Algorithm Execution:**
- Location: `TensorizedPauliDecomposition.py`
- Triggers: Import and call `PauliDecomposition(matrix, sparse=False, output="Lists")`
- Responsibilities: Main decomposition, argument validation, format selection

**Test Suite:**
- Location: `TestSuite.py` line 35
- Triggers: Direct execution (`python TestSuite.py`)
- Responsibilities: Generate test matrix, call both methods, print comparison result

**Benchmarking Script:**
- Location: `Benchmarking.py` lines 59-101
- Triggers: Direct execution (`python Benchmarking.py`)
- Responsibilities: Multi-algorithm comparison, output file generation, statistical analysis

**TFIM Hamiltonian:**
- Location: `TFIM.py`
- Triggers: Import and call `tfimHamiltonian(dim)` for test matrix generation
- Responsibilities: Construct transverse field Ising model Hamiltonian

## Error Handling

**Strategy:** Minimal explicit error handling; relies on NumPy/SciPy exceptions and type errors

**Patterns:**
- Sparse matrix format conversion attempts catch exceptions (line 49-52 in TensorizedPauliDecomposition.py) to handle both NumPy and tensor-like inputs
- Matrix dimension validation through math.ceil/log (implicit assumption: matrix is square)
- Coefficient comparison uses epsilon tolerance (line 31 in TestSuite.py): `eps = 10**(-5)`
- Zero-checking prevents unnecessary recursion (lines 79-84 in TensorizedPauliDecomposition.py)

## Cross-Cutting Concerns

**Logging:** None - Silent execution with optional console output controlled by `out` and `debug` flags in Benchmarking.py (lines 20-21)

**Validation:**
- Matrix dimension check (must be square)
- Matrix format validation (NumPy array or SciPy sparse)
- Coefficient epsilon tolerance for numerical comparisons

**Performance Optimization:**
- Sparse matrix support flag enables sparse arithmetic
- Zero coefficient pruning prevents unnecessary recursion branches
- Tensor slicing operations extract only needed submatrices

**Output Control:**
- `output` parameter in PauliDecomposition: "Lists" returns [strings, coeffs], string format returns concatenated output
- Optional file writing in Benchmarking.py with time-series data

---

*Architecture analysis: 2026-02-12*
