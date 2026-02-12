# PauliDecomposition Readability Refactor

## What This Is

A readability refactor of the Tensorized Pauli Decomposition codebase — a Python implementation of a recursive algorithm that decomposes matrices into sums of Pauli operator terms. The goal is to make the code clear and well-documented for physicists and contributors who want to understand, use, or extend the algorithm, without changing any behavior.

## Core Value

The code must remain functionally identical while becoming significantly easier to read, understand, and contribute to for quantum computing researchers.

## Requirements

### Validated

<!-- Existing capabilities inferred from codebase -->

- Pauli decomposition of arbitrary square matrices via recursive tensor factorization — existing
- Support for both dense (NumPy) and sparse (SciPy) matrix input — existing
- Padding to power-of-2 dimensions for non-power-of-2 matrices — existing
- Validation test suite comparing TPD output against Qiskit SparsePauliOp — existing
- Benchmarking harness comparing TPD against multiple quantum frameworks (Qiskit, PennyLane, Cirq, H2ZIXY, pauli_decomposer) — existing
- TFIM Hamiltonian generator for test data — existing

### Active

- [ ] Clean up naming conventions (variables, functions) for consistency and clarity
- [ ] Add docstrings, comments, and type hints across all modules
- [ ] Restructure code organization (files/modules) if it improves clarity
- [ ] Refactor tests for consistency and readability alongside the code
- [ ] Expand README with usage examples and API reference for all public functions

### Out of Scope

- Behavior changes — the algorithm output must remain identical for all inputs
- Performance optimization — this is purely a readability effort
- Adding new algorithms or decomposition methods
- Math/theory background in README — the audience (physicists) already knows the theory
- New testing frameworks — keep custom test approach, just clean it up

## Context

- Flat single-directory Python project with 4 core files: `TensorizedPauliDecomposition.py`, `TestSuite.py`, `Benchmarking.py`, `TFIM.py`
- No package structure, no build system, no type hints currently
- Naming is inconsistent: mix of PascalCase, camelCase, and snake_case across functions and variables
- No docstrings on any functions
- Existing tests use custom comparison logic (not pytest/unittest)
- The project has an associated academic paper (arXiv/journal publication) referenced in README
- Benchmarking depends on several external quantum libraries (Qiskit, PennyLane, Cirq, QuTiP, H2ZIXY, pauli_decomposer)

## Constraints

- **No behavior changes**: All existing tests must pass after refactoring (with updated test code)
- **Audience**: Physicists and open-source contributors — use domain-appropriate naming
- **Python**: Stay pure Python, no new dependencies

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Reorganize file structure if it helps clarity | User approved restructuring | — Pending |
| Refactor tests alongside code | Keep tests consistent with refactored code | — Pending |
| Skip math background in README | Target audience already knows Pauli decomposition | — Pending |

---
*Last updated: 2026-02-12 after initialization*
