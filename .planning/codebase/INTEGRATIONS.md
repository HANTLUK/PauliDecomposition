# External Integrations

**Analysis Date:** 2026-02-12

## APIs & External Services

**Quantum Computing Frameworks:**
- Qiskit - Reference Pauli decomposition implementation
  - SDK/Client: `qiskit.quantum_info.SparsePauliOp`, `qiskit.quantum_info.operators`
  - Usage: `SparsePauliOp.from_operator()` for validation in `TestSuite.py` and benchmarking
  - Files: `TestSuite.py`, `Benchmarking.py`

- PennyLane - Quantum machine learning with Pauli decomposition
  - SDK/Client: `pennylane`, `pennylane.pauli_decompose`
  - Usage: Alternative algorithm comparison in benchmarking suite
  - Files: `Benchmarking.py`

- Cirq - Google quantum computing framework
  - SDK/Client: `cirq.pauli_expansion`
  - Usage: Alternative Pauli decomposition algorithm for performance comparison
  - Files: `Benchmarking.py`

- QuTiP - Quantum Toolbox in Python
  - SDK/Client: `qutip` (imported as `qt`)
  - Usage: Generates quantum operators and TFIM Hamiltonian test matrices
  - Files: `TFIM.py`

**Algorithm Reference Implementations:**
- H2ZIXY - Custom H2ZIXY algorithm module
  - SDK/Client: `H2ZIXY` class/function
  - Usage: Benchmarking comparison method in `Benchmarking.py`
  - Files: `Benchmarking.py`

- Pauli Decomposer - Paper implementation of alternative decomposition
  - SDK/Client: `PauliDecomposer` class/function
  - Usage: Benchmarking comparison (labeled as "PC" in results)
  - Files: `Benchmarking.py`

## Data Storage

**Databases:**
- None - Project uses in-memory matrix operations only

**File Storage:**
- Local filesystem only
- Output format: `.dat` files for benchmark results
  - Location: Generated in working directory with pattern `{TestName}.dat`
  - Format: Tab-separated values with timing data
  - Files: `Benchmarking.py` writes to files like `"Random Matrix.dat"`, `"Unit Matrix.dat"`

**Caching:**
- None detected

## Authentication & Identity

**Auth Provider:**
- Not applicable - No authentication required
- All integrations are library-based with no external API keys or credentials

## Monitoring & Observability

**Error Tracking:**
- None - No error tracking service integrated
- Custom try-except blocks in `TensorizedPauliDecomposition.py` for handling matrix operations

**Logs:**
- Console output via `print()` statements
- Benchmark results written to `.dat` files
- Debug flags in `Benchmarking.py`: `debug = 0`, `out = 1` control console output

## CI/CD & Deployment

**Hosting:**
- Local development only - No remote deployment
- GitHub repository for version control (`.git` present)

**CI Pipeline:**
- None detected - No GitHub Actions, Jenkins, or other CI service configured

## Environment Configuration

**Required env vars:**
- None - Project has no environment variable dependencies

**Secrets location:**
- Not applicable - No secrets or credentials required

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

## Data Flow

**Algorithm Validation:**
1. `TestSuite.py` generates random test matrices
2. Runs decomposition through `TensorizedPauliDecomposition.PauliDecomposition()`
3. Validates against Qiskit's `SparsePauliOp.from_operator()` reference implementation
4. Compares Pauli strings and coefficients with epsilon tolerance (1e-5)

**Benchmarking Workflow:**
1. `Benchmarking.py` generates test matrices using functions in `TFIM.py` and local generators
2. Executes multiple algorithms:
   - `H2ZIXY()` from external module
   - `qml.pauli_decompose()` from PennyLane
   - `SparsePauliOp.from_operator()` from Qiskit
   - `cirq.pauli_expansion()` from Cirq
   - `PauliDecomposer()` from external module
3. Measures execution time across `stat_runs` iterations (default: 2)
4. Writes timing data to `.dat` files for each test type

**TFIM Hamiltonian Generation:**
1. `TFIM.py` uses QuTiP to create spin operators
2. Constructs tensor products for N-qubit systems
3. Builds Hamiltonian matrix representation

## External Dependencies Summary

**Scientific Computing Stack:**
- numpy, scipy for matrix operations
- matplotlib for visualization

**Quantum Computing Integration:**
- Qiskit, PennyLane, Cirq, QuTiP for algorithm comparison and validation
- No real quantum hardware integration (classical simulation only)

**No Cloud/SaaS Integration:**
- Project is completely self-contained
- All computations run locally
- No API calls to remote services
- No database connections

---

*Integration audit: 2026-02-12*
