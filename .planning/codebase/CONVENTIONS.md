# Coding Conventions

**Analysis Date:** 2026-02-12

## Naming Patterns

**Files:**
- PascalCase for main module files: `TensorizedPauliDecomposition.py`, `TestSuite.py`, `Benchmarking.py`, `TFIM.py`
- Core algorithm file uses descriptive name reflecting its primary function

**Functions:**
- Mix of naming styles observed:
  - camelCase: `PauliDecomposition()`, `randomMatrix()`, `tfimHamiltonian()`, `sparseRandom()`, `hermRandom()`, `symmRandom()`
  - Snake_case: `spin_operator()`, `test1()`, `test2()`, `stat_runs`, `start_time`, `output_line`
  - PascalCase: `PauliDecSparse()`, `TestMatrices`, `CompareMethods`, `ExecuteTests`, `MethodsName`, `MaxSizes`
- Descriptive names matching function purpose

**Variables:**
- Global configuration variables use lowercase: `out`, `debug`, `stat`, `stat_runs`, `timeBarrier`
- Dictionary keys use lowercase: `"rand"`, `"diag"`, `"herm"`, `"spars"`, `"symm"`, `"unit"`, `"tfim"`
- Local variables use snake_case: `start_time`, `output_line`, `elapsed`, `nonZero`, `matDim`, `qBitDim`, `padDim`, `halfDim`
- Mixed camelCase/PascalCase in dictionary names: `CompareMethods`, `ExecuteTests`, `Methods`, `MethodsName`, `MaxSizes`, `Tests`, `TestMatrices`, `Results`
- Abbreviated variable names used: `coeff1`, `coeffX`, `coeffY`, `coeffZ`, `coefficients`, `mat`, `dim`

**Types:**
- No type hints used in codebase
- Parameter names suggest expected types: `matrix`, `dim`, `sparse`, `PauliStringInit`, `output`

## Code Style

**Formatting:**
- Indentation: Tabs used throughout (observed in all files)
- No enforced style tool detected (no `.prettierrc`, `black` config, or `autopep8` setup)
- Inconsistent spacing around operators:
  - `0.5*(matrix[0:halfDim, 0:halfDim] + matrix[halfDim:, halfDim:])` - no spaces around `*`
  - `2**qBitDim` - no spaces around `**`
  - Conditional spacing varies: `if sparse:` vs `if nonZero != 0:`

**Linting:**
- No linting configuration detected (no `.flake8`, `.pylintrc`, or `setup.cfg`)
- Code has style inconsistencies that suggest no active linting

## Import Organization

**Order:**
1. Standard library imports: `import numpy as np`, `import scipy.sparse as sp`, `import math`, `import timeit`, `import time`
2. Third-party library imports: `import matplotlib.pyplot as plt`, `import statistics`, `import io`
3. Domain-specific imports: `import cirq`, `import pennylane as qml`, `from qiskit.quantum_info import SparsePauliOp`
4. Local module imports: `from TensorizedPauliDecomposition import PauliDecomposition`, `from TFIM import tfimHamiltonian`

**Path Aliases:**
- Standard aliases used: `np` for numpy, `sp` for scipy.sparse, `qml` for pennylane, `qt` for qutip
- Aliases applied inconsistently in Benchmarking.py where `pennylane.numpy` is imported separately: `from pennylane import numpy as np`

## Error Handling

**Patterns:**
- Bare `except:` blocks used in `TensorizedPauliDecomposition.py` lines 49-52:
  ```python
  try:
      Coeffs.append(matrix[0,0])
  except:
      Coeffs.append(matrix[0,0].numpy())
  ```
- No explicit error types caught - broad exception handling for TensorFlow tensor compatibility
- No error messages or logging in exception blocks
- No assertions for input validation

## Logging

**Framework:** Console output only - no logging framework detected

**Patterns:**
- Conditional printing using module-level `out` variable in `Benchmarking.py`:
  ```python
  if out: print(f"{Tests[Test]}:")
  if out: print(f"{Method}:")
  if out: print("dim",n,": ",elapsed)
  ```
- Print statements used for debugging and output: `print(comparison(test1,test2,testMatrix))`
- No structured logging or log levels used

## Comments

**When to Comment:**
- Inline comments used for clarification: `# H2ZIXY Algorithm`, `# Pauli Decomposer Paper`
- Section comments separate logical blocks: `# Pad, if dimension is not a power of 2`, `# Output for dimension 1`, `# Calculates the tensor product coefficients...`
- Comment frequency is moderate - approximately one comment per 10-15 lines of code

**JSDoc/TSDoc:**
- Single docstring used only in main algorithm function `PauliDecomposition()` at `TensorizedPauliDecomposition.py` lines 6-22
- Docstring format uses Google-style Args and Returns sections
- No docstrings on helper functions or test functions
- Module-level docstring only in `Benchmarking.py` line 17

## Function Design

**Size:**
- Small utility functions: 1-3 lines (e.g., `identityMatrix()`, `diagRandom()`)
- Medium functions: 5-15 lines (e.g., `test1()`, `test2()`, `comparison()`)
- Large recursive functions: 50+ lines (e.g., `PauliDecomposition()` is 97 lines)

**Parameters:**
- Optional parameters with defaults used: `PauliDecomposition(matrix, sparse=False, PauliStringInit="", output="Lists")`
- No keyword-only parameters (using `/` or `*`)
- Positional parameters common: `def comparison(method1, method2, matrix):`
- No *args or **kwargs patterns used

**Return Values:**
- Lists returned from functions: `return [list1, coeffs1]`
- Tuples unpacked on call: `list1, coeffs1 = PauliDecomposition(matrix)`
- Multiple values returned as lists/tuples
- Strings returned from some branches: `return outputString`
- `None` implicitly returned in error branches without explicit return

## Module Design

**Exports:**
- No explicit `__all__` definitions observed
- Main function is `PauliDecomposition()` in `TensorizedPauliDecomposition.py`
- Functions exported through direct imports: `from TensorizedPauliDecomposition import PauliDecomposition`
- Test functions prefixed with `test`: `test1()`, `test2()` in `TestSuite.py`

**Barrel Files:**
- No barrel files (`__init__.py`) detected - flat module structure
- Each file is standalone executable script or importable module
- Direct module imports without package structure

---

*Convention analysis: 2026-02-12*
