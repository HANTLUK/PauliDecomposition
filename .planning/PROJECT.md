# PauliDecomposition Readability Refactor

## What This Is

A well-documented Python implementation of the Tensorized Pauli Decomposition algorithm — a recursive method that decomposes matrices into sums of Pauli operator terms. The codebase features consistent PEP 8 naming, comprehensive docstrings with type hints, and a complete README with usage examples and API reference for physicists and contributors.

## Core Value

The code must remain functionally identical while becoming significantly easier to read, understand, and contribute to for quantum computing researchers.

## Requirements

### Validated

- Pauli decomposition of arbitrary square matrices via recursive tensor factorization — existing
- Support for both dense (NumPy) and sparse (SciPy) matrix input — existing
- Padding to power-of-2 dimensions for non-power-of-2 matrices — existing
- Validation test suite comparing TPD output against Qiskit SparsePauliOp — existing
- Benchmarking harness comparing TPD against multiple quantum frameworks — existing
- TFIM Hamiltonian generator for test data — existing
- ✓ Clean up naming conventions (variables, functions) for consistency and clarity — v1.0
- ✓ Add docstrings, comments, and type hints across all modules — v1.0
- ✓ Restructure code organization (entry point guards) for clarity — v1.0
- ✓ Refactor tests for consistency and readability alongside the code — v1.0
- ✓ Expand README with usage examples and API reference for all public functions — v1.0

### Active

(None — v1.0 milestone complete. Define new requirements with `/gsd:new-milestone`.)

### Out of Scope

- Behavior changes — the algorithm output must remain identical for all inputs
- Performance optimization — this is purely a readability effort
- Adding new algorithms or decomposition methods
- Math/theory background in README — the audience (physicists) already knows the theory
- New testing frameworks — keep custom test approach, just clean it up

## Context

Shipped v1.0 with 634 LOC Python across 4 core files:
- `TensorizedPauliDecomposition.py` — core algorithm (146 LOC)
- `Benchmarking.py` — performance comparison harness (265 LOC)
- `TestSuite.py` — validation test suite (134 LOC)
- `TFIM.py` — TFIM Hamiltonian generator (89 LOC)

All functions use snake_case naming, have NumPy-style docstrings with type hints, and entry points are guarded with `__name__` checks. README provides installation, 5 usage examples, and API reference for all 15 public functions.

## Constraints

- **No behavior changes**: All existing tests must pass after refactoring (with updated test code)
- **Audience**: Physicists and open-source contributors — use domain-appropriate naming
- **Python**: Stay pure Python, no new dependencies

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Reorganize file structure if it helps clarity | User approved restructuring | ✓ Good — added `__name__` guards, kept flat structure |
| Refactor tests alongside code | Keep tests consistent with refactored code | ✓ Good — tests use same conventions as production code |
| Skip math background in README | Target audience already knows Pauli decomposition | ✓ Good — README focuses on usage and API |
| Use full descriptive names over abbreviations | Clarity for domain experts | ✓ Good — e.g., `qubit_dim` not `qBitDim` |
| NumPy-style docstring format | Most familiar to scientific Python community | ✓ Good — consistent across all modules |
| Use `decompose_with_*` prefix for test wrappers | Distinguish helper wrappers from actual test assertions | ✓ Good — function names now reflect roles |
| Document tolerance values inline | Explain why specific precision thresholds are chosen | ✓ Good — 1e-5 rationale documented |

---
*Last updated: 2026-02-13 after v1.0 milestone*
