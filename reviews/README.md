# Reviews — PyBackup

Public product review surface for `py-backup` (peer of `tests/`).

| File | Role |
|------|------|
| `what-to-review.md` | Living review plan / checklist |
| `test-plan.md` | TP-* status map of the previous shell suite. The Python suite is `tests/test_pybackup.py` |
| `requirement-test-matrix.md` | Requirement → TP families. Those TP ids are the previous shell suite |
| `lessons.md` | Durable failure modes to re-check |
| `index.md` | Report index |
| `reports/` | Dated review run reports |

**Ship unit:** `src/PyBackup` (**1.0.0**)  
**Command:** `py-backup`  
**Suite:** `sh tests/run.sh`  
**Last suite baseline:** 2026-10-22, 24 tests, OK  

**Privilege review focus:** grant trust, `generate-sudoer-request`, `submit-sudoer-request`, `print-sudoers`, `print-sudoers-install-script`, and `remove-project-sudoers` (draft only).
