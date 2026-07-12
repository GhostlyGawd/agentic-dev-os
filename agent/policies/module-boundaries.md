# Module Boundary Policy

Architecture boundaries are declared in `architecture.json` and checked by `tests/test_architecture.py`.

- Imports must point only to declared dependencies or the Python standard library.
- Internal modules are not public APIs.
- Cycles are prohibited.
- Cross-cutting shared behavior belongs in a deliberately owned module.
- A boundary exception needs a decision record, owner, and expiry date.
