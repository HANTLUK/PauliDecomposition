# Roadmap: PauliDecomposition Readability Refactor

## Overview

Transform a working quantum computing research codebase into a readable, well-documented implementation that physicists and contributors can easily understand and extend. Three phases cover the complete refactor: standardize code structure and naming, add comprehensive documentation with type hints, and polish tests plus README with usage examples. No behavior changes - all existing functionality must remain identical.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Code Foundation** - Standardize naming conventions and reorganize code structure
- [ ] **Phase 2: Documentation** - Add docstrings, type hints, and inline comments
- [ ] **Phase 3: Tests & README** - Refactor tests and expand README with examples and API reference

## Phase Details

### Phase 1: Code Foundation
**Goal**: Code uses consistent naming conventions and logical organization
**Depends on**: Nothing (first phase)
**Requirements**: NAME-01, NAME-02, NAME-03, STRC-01, STRC-02, STRC-03
**Success Criteria** (what must be TRUE):
  1. All function names follow snake_case convention consistently across all modules
  2. All variable names use descriptive, domain-appropriate terminology (e.g., qubit_dim instead of qBitDim)
  3. Constants use UPPER_SNAKE_CASE throughout the codebase
  4. Related utility functions are grouped logically (matrix generators together, spin operators together, etc.)
  5. Entry points (test execution, benchmarking) are clearly separated from library code
**Plans**: 4 plans in 2 waves

Plans:
- [x] 01-01-PLAN.md - Rename core algorithm module (TensorizedPauliDecomposition.py)
- [x] 01-02-PLAN.md - Rename test and utility modules (TestSuite.py, TFIM.py)
- [x] 01-03-PLAN.md - Rename benchmarking module and verify refactoring
- [x] 01-04-PLAN.md - Add `__name__` guards to separate entry points from library code (STRC-03)

### Phase 2: Documentation
**Goal**: Every function and complex algorithm step is documented with type hints
**Depends on**: Phase 1
**Requirements**: DOCS-01, DOCS-02, DOCS-03
**Success Criteria** (what must be TRUE):
  1. Every public function has a docstring explaining what it does, its parameters, return values, and includes an example
  2. Complex algorithm sections (tensor factorization, recursion logic) have inline comments explaining the math and logic
  3. All function signatures include type hints for parameters and return values
**Plans**: TBD

Plans:
- TBD (defined during plan-phase)

### Phase 3: Tests & README
**Goal**: Tests are readable and README provides complete usage guidance
**Depends on**: Phase 2
**Requirements**: TEST-01, TEST-02, TEST-03, READ-01, READ-02, READ-03
**Success Criteria** (what must be TRUE):
  1. Test function names clearly describe what is being validated (e.g., test_random_matrix_equivalence)
  2. Test code follows the same naming and documentation standards as main code
  3. Test assertions and comparisons include comments explaining validation logic
  4. README includes usage examples showing how to call PauliDecomposition with different input types
  5. README includes API reference documenting all public functions with their parameters
  6. README includes installation and dependency instructions
**Plans**: TBD

Plans:
- TBD (defined during plan-phase)

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Code Foundation | 4/4 | ✓ Complete | 2026-02-12 |
| 2. Documentation | 0/TBD | Not started | - |
| 3. Tests & README | 0/TBD | Not started | - |

---
*Roadmap created: 2026-02-12*
*Last updated: 2026-02-12 - Phase 1 complete*
