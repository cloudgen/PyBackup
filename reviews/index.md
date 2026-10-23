# Review reports index — PyBackup

**Current product (2026-10-22):** PyBackup **1.0.0**, command `py-backup`, ship unit `src/PyBackup`. Front rows are client-side (**1**), system-log (**3**), language (**4**), sudoers (**5**), self-management (**8**), and Exit (**9**). Findings for that command are `docs/reviews/2026-10-22-pybackup-bootstrap-review.md` (Revise: open P2, no P0/P1). Python suite: 24 tests, OK.

Older rows in the table are earlier reviews of this repository. The current command is `py-backup`.

| Date | Report | Scope | Verdict | Suite |
|------|--------|-------|---------|-------|
| 2026-10-22 | `docs/reviews/2026-10-22-pybackup-bootstrap-review.md` | HelloTui → PyBackup; folder backup on the text menu and on argv | Revise (open P2, no P0/P1) | 1.0.0 Python 24 tests OK. Shell runner not run. |
| 2026-10-14 | `reports/2026-10-14-requirement-coverage-menu-and-os.md` | Front **5**/**6**/**7** and eight OS family labels | Sufficient with Gaps | 1.26.0 PASS=610 FAIL=0 SKIP=2 |
| 2026-09-30 | `reports/2026-09-30-requirement-coverage-menu-contract.md` | C-menu after named menu off a terminal stops, empty front leaves, and row 82 runs about | Sufficient with Gaps | 1.20.0 PASS=473 FAIL=0 SKIP=2 |
| 2026-09-30 | `reports/2026-09-30-requirement-coverage-zero-cli-verb.md` | C-full-product after non-interactive zero-cli-verb became self-install | Sufficient with Gaps | 1.19.0 PASS=455 FAIL=0 SKIP=2 |
| 2026-09-30 | `reports/2026-09-30-requirement-coverage-main-menu.md` | C-full-product after the numbered-board menu | Sufficient with Gaps | 1.18.0 PASS=436 FAIL=0 SKIP=2 |
| 2026-09-27 | `reports/2026-09-27-checklist-temp-file-system-cache-folder.md` | CL-TEMP-FILE-SYSTEM cache folder; storage law 1.4.0; TP-CLI-06/12 | **Pass** | 1.16.5 PASS=410 FAIL=0 SKIP=2 |
| 2026-09-06 | `reports/2026-09-06-requirement-coverage-human-readability.md` | C-full-product coverage + README/REQ human-facing; TP-CLI-17 have; coding-style + sudo-command REQs; wrap/detect/TP-27 Gaps | Sufficient with Gaps | 1.16.3 |
| 2026-08-28 | `reports/2026-08-28-requirement-coverage-case2.md` | C-full-product coverage + test plan; case 2 empty argv; Gaps TP-CLI-17 / TP-27 / coding-style REQ | Sufficient with Gaps | 1.12.0 |
| 2026-08-28 | `cli-routed-verb-table.md` | Live dispatcher inventory; case 2 TTY empty argv = numbered list | living | 1.12.0 |
| 2026-08-23 | `cli-routed-verb-table.md` | Live dispatcher inventory + human-readable `verb: explain`; test-purpose grant-emit verbs; `menu`/`main` routed | living | 1.11.0 |
| 2026-08-17 | `reports/2026-08-17-review-revision-test-plans.md` | Review/test-plan revision vs 1.9.0 generate + operator-readable errors | **PASS** (plans aligned; suite green) | PASS=242 FAIL=0 SKIP=2 |
| 2026-08-17 | 1.9.0 generate-sudoer-request | Local verified compact JSON; submit compact handoff; TP-24 | living | 1.9.0 |
| 2026-08-17 | INC-20260817-002 | Submit fail-closed error not human-readable; incomplete JSON not a standing class | living | 1.8.2 |
| 2026-08-17 | `reports/2026-08-17-requirement-coverage.md` | C-full-product sufficient-check + AC↔TP | **Sufficient with Gaps** (FB-COV-01..06) | PASS=209 FAIL=0 SKIP=2 |
| 2026-08-17 | host-probe submit **update** | Default `update` when `/etc/sudoers.d/{{APP_NAME}}-<user>` exists; TP-23/23b; AC-22 | living | 1.8.2 |
| 2026-08-17 | `reports/2026-08-17-json-reencode-fidelity.md` | JSON re-encode / inbound **JR-1..8**; suite 22e/22f | **PASS** (FB-JR-01 host inbound residual) | PASS=198 FAIL=0 SKIP=2 |
| 2026-08-17 | `what-to-review` **JR-1..8** | Review plan gate: JSON re-encode / inbound fidelity (pretty convert + submit + S15) | living | PASS=198 FAIL=0 SKIP=2 |
| 2026-08-17 | INC-20260817-001 knowledge lock | Re-encode fidelity: REQ 1.1.0 / three-layer 1.7.0 / S15 / TP-22e/22f | living | PASS=198 FAIL=0 SKIP=2 |
| 2026-08-15 | `reports/2026-08-15-sudoer-json-file.md` | JSON sudoer file = `folder-backup` only; emit 1.8.0 | **PASS** (FB-SUDOER-01 residual runtime) | PASS=189 FAIL=0 SKIP=2 |
| 2026-08-15 | `reports/2026-08-15-coverage-public-inbound.md` | Coverage P0–P2 + public inbound detect | **PASS** (findings closed) | PASS=175 FAIL=0 SKIP=2 |
| 2026-08-13 | `reports/2026-08-13-bootstrap-specialize-cli-template.md` | Origin retarget A=cli-template → B; VERSION 1.6.1 alignment | **PASS** | PASS=157 FAIL=0 SKIP=2 |
| 2026-08-12 | **1.6.0 retention** (daily 5 + total 30; TP-17/18; retention REQs) | `fb_apply_retention` + deposit Type 0 when writable + sudoers rm | **PASS** | PASS=166 FAIL=0 SKIP=0 |
| 2026-08-12 | **1.5.0 restore dest whitelist** (W-ETC-USER; mold/REQ/TP-16; INC-20260812-001 Closed) | `fb_refuse_restore_dest`; checklist `docs/checklists/2026-08-12-checklist-restore-dest-whitelist-w-etc-user.md` | **PASS** | PASS=156 FAIL=0 SKIP=0 |
| 2026-08-11 | **Housekeeping** (version surfaces + lessons residual) | README/SECURITY → 1.4.4; L-SUDOERS-05 renumber; L-PUSH-VAULT-01 | living | PASS=138 FAIL=0 SKIP=2 |
| 2026-08-09 | **Review plans updated** (`what-to-review.md`, `test-plan.md`, `requirement-test-matrix.md`, `lessons.md`) | Plans for 1.4.4 multi-user project-sudoers-file | living | PASS=138 FAIL=0 SKIP=2 |
| 2026-08-09 | `reports/2026-08-09-security-review-folder-backup.md` | Full security review (design + host) | **Pass (design) / Revise (host)** | F1–F8; host still test_local |
| 2026-08-09 | `reports/2026-08-09-sudoers-security-folder-backup.md` | Sudoers security (trust tiers) | **Pass (test only)** | supersedes 2026-08-03 production claim for local-only |
| 2026-08-03 | `reports/2026-08-03-product-review-initial.md` | Full product (law + ship unit + suite) | **Revise** (docs gaps; core suite green) | PASS=82 FAIL=0 SKIP=2 |
| 2026-08-03 | `reports/2026-08-03-sudoers-security-folder-backup.md` | Sudoers security (pre-emit) | **Pass (historical; superseded for production)** | local-only; see 2026-08-09 |
