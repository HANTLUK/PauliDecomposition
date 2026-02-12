# Testing Patterns

**Analysis Date:** 2026-02-12

## Test Framework

**Runner:**
- No formal test framework configured (no pytest, unittest discovery, or test runner config)
- Tests executed directly as Python scripts

**Assertion Library:**
- No assertion library used - manual comparison checks
- Boolean return values used for validation: `return equal` in `TestSuite.py`

**Run Commands:**
```bash
python TestSuite.py              # Run comparison test
python Benchmarking.py           # Run performance benchmarks
```

## Test File Organization

**Location:**
- Tests co-located with source code in same directory
- `TestSuite.py` file in project root alongside main modules
- No separate `tests/` directory structure

**Naming:**
- Test file: `TestSuite.py` (PascalCase, matches module naming convention)
- Test functions: `test1()`, `test2()`, lowercase with numeric suffix
- Helper comparison function: `comparison()` (descriptive verb-based name)

**Structure:**
```
PauliDecomposition/
├── TensorizedPauliDecomposition.py    # Main algorithm
├── TestSuite.py                       # Tests and verification
├── Benchmarking.py                    # Performance tests
├── TFIM.py                            # Test data generators
└── .planning/
    └── codebase/
```

## Test Structure

**Suite Organization:**
```python
# From TestSuite.py

def test2(matrix):
    testResult2 = SparsePauliOp.from_operator(matrix)
    coeffs2 = testResult2.coeffs
    list2 = testResult2.paulis
    return [list2,coeffs2]

def test1(matrix):
    list1, coeffs1 = PauliDecomposition(matrix)
    return [list1,coeffs1]

def randomMatrix(dim):
    return np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))

testMatrix = randomMatrix(4)

def comparison(method1, method2, matrix):
    list1,coeffs1 = method1(matrix)
    list2,coeffs2 = method2(matrix)
    equal = True
    for x,y in zip(list1,list2):
        if str(x) != str(y):
            equal = False
    eps = 10**(-5)
    for x,y in zip(coeffs1,coeffs2):
        if abs(complex(x) - complex(y)) > eps:
            equal = False
    return equal

print(comparison(test1,test2,testMatrix))
```

**Patterns:**
- No setUp/tearDown - test data generated inline with `randomMatrix()`
- Tests are functions that wrap algorithm implementations
- Comparison performed with manual loops and threshold checks (epsilon = 1e-5)
- Results printed to stdout: `print(comparison(test1,test2,testMatrix))`
- Test matrix generation: `testMatrix = randomMatrix(4)` - single 4x4 complex matrix
- No parameterized tests or test generators

## Mocking

**Framework:** No mocking framework used

**Patterns:**
- Reference implementation used for comparison: `SparsePauliOp.from_operator()` from Qiskit
- Two implementations compared: custom implementation (`test1`) vs reference (`test2`)
- No mocking of external dependencies

**What to Mock:**
- External quantum libraries could be mocked if testing needs to be isolated
- Currently Qiskit used directly for reference validation

**What NOT to Mock:**
- Core algorithm implementation must be tested with real matrix operations
- Reference implementations should be actual implementations for validation

## Fixtures and Factories

**Test Data:**
```python
# From TestSuite.py
def randomMatrix(dim):
    return np.add(np.random.rand(dim,dim),1.j*np.random.rand(dim,dim))

testMatrix = randomMatrix(4)
```

**From Benchmarking.py:**
```python
def diagRandom(dim):
    return np.add(np.zeros([dim,dim]),np.diag(np.add(np.random.rand(dim),1.j*np.random.rand(dim))))

def identityMatrix(dim):
    return np.identity(dim)

def sparseRandom(dim):
    return sp.random(dim,dim,density=1./dim,format="csr")

def symmRandom(dim):
    rand = randomMatrix(dim)
    return np.add(rand,np.transpose(rand))

def hermRandom(dim):
    rand = randomMatrix(dim)
    return np.add(rand,rand.conjugate().transpose())

def oneTerm(dim):
    rand = randomMatrix(2)
    return np.kron(rand,np.eye(int(dim/2)))

TestMatrices = {
    "diag": diagRandom,
    "unit": identityMatrix,
    "rand": randomMatrix,
    "spars": sparseRandom,
    "herm": hermRandom,
    "symm": symmRandom,
    "tfim": tfimHamiltonian,
    "oneTerm": oneTerm
}
```

**Location:**
- Test data generators live in same module as tests
- Matrix factory functions defined with descriptive names
- Dictionary mapping test names to factory functions: `TestMatrices`
- TFIM Hamiltonian data from separate `TFIM.py` module

## Coverage

**Requirements:** Not enforced - no coverage configuration or metrics

**View Coverage:**
- No coverage measurement tool configured
- No baseline or target coverage specified

## Test Types

**Unit Tests:**
- Comparison tests verify algorithm correctness: `comparison(method1, method2, matrix)` in `TestSuite.py`
- Tests focused on output format and numerical accuracy
- Single assertion: output matches reference implementation within epsilon tolerance (1e-5)
- Scope: Algorithm output validation against Qiskit reference

**Integration Tests:**
- Benchmarking tests exercise full algorithm against different matrix types
- Test multiple methods together: H2ZIXY, PennyLane, Qiskit, Cirq, PauliDecomposer
- Tests interaction with different library implementations in `Benchmarking.py` lines 59-101
- Matrix types tested: diagonal, Hermitian, symmetric, random, sparse, identity, TFIM, single-term

**E2E Tests:**
- Not explicitly defined as separate test type
- Benchmarking serves as full end-to-end validation with real quantum matrix instances
- TFIM Hamiltonian from `TFIM.py` provides realistic test case

## Common Patterns

**Async Testing:**
- Not applicable - no async/await patterns in codebase

**Error Testing:**
- No explicit error case testing
- Bare `except:` in main algorithm handles edge cases gracefully without testing them
- Bare exception at `TensorizedPauliDecomposition.py` lines 49-52:
  ```python
  try:
      Coeffs.append(matrix[0,0])
  except:
      Coeffs.append(matrix[0,0].numpy())
  ```
- This pattern accommodates TensorFlow tensors but is not explicitly tested

**Numerical Tolerance Testing:**
- Epsilon-based comparison used: `eps = 10**(-5)`
- Complex number comparison with absolute difference threshold:
  ```python
  if abs(complex(x) - complex(y)) > eps:
      equal = False
  ```
- String comparison for Pauli operators: `if str(x) != str(y):`

**Performance Testing:**
- Benchmarking framework in `Benchmarking.py` measures execution time
- `timeit.default_timer()` used for precise timing
- Multiple runs with statistical analysis:
  ```python
  elapsed = []
  for i in range(stat_runs):
      start_time = timeit.default_timer()
      Methods[Method](matrix)
      elapsed.append((timeit.default_timer() - start_time))
  mean = statistics.mean(elapsed)
  ```
- Results written to `.dat` files for analysis: `f"{Tests[Test]}.dat"`
- Time barriers used to stop testing slow methods: `if mean > timeBarrier: break` (10 second default)

## Known Testing Limitations

**No Framework:**
- Tests cannot be discovered or run automatically
- No test isolation or ordering guarantees
- No parallel test execution
- No detailed failure reporting

**Limited Coverage:**
- Single 4x4 test matrix in `TestSuite.py`
- Only two implementations compared (custom vs Qiskit)
- No edge case testing (empty matrices, singular matrices, etc.)
- No error condition testing

**Benchmark Constraints:**
- Benchmarks only measure full algorithm execution
- No profiling of individual algorithm steps
- Time barrier hard stops tests rather than capturing complete performance curve
- Results stored in text files requiring manual analysis

---

*Testing analysis: 2026-02-12*
