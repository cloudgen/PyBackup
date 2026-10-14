# Reviews — folder-backup

Public product review surface (peer of `tests/`).

| File | Role |
|------|------|
| `what-to-review.md` | Living review plan / checklist |
| `test-plan.md` | TP-* status map |
| `requirement-test-matrix.md` | Requirement → TP families |
| `lessons.md` | Durable failure modes to re-check |
| `index.md` | Report index |
| `reports/` | Dated review run reports |

**Ship unit:** `src/folder-backup` (**VERSION 1.26.0**)  
**Suite:** `./tests/run.sh`  
**Last suite baseline:** see `test-plan.md` (1.26.0: PASS=610 FAIL=0 SKIP=2)  

**Privilege review focus (1.9.0):** trust tier **S13**, project-sudoers-file, **independent generate** (`generate-sudoer-request` AC-23/24 · S16), `submit-sudoer-request` public inbound, **host-probe add/update (AC-22)**, inbound fidelity (AC-21), **operator-readable errors** (TP-25), `print-sudoers-install-script`, `remove-project-sudoers` (draft only).
