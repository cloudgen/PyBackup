# Requirements

Authoritative specialized product law for **PyBackup** lives here.

**Current state (2026-10-23):** Specialized **software-development** product. Left genesis. Bootstrap parent is **HelloTui**. The command is `py-backup`. A terminal with no command opens the numbered boards. Front rows are client-side **1**, system-log **3**, language **4**, sudoers **5**, self-management **8**, and Exit **9**. No terminal with no command prints help and returns 0. Pip lifecycle is `python -m pip` (rows **82**–**87**). There is no `curl | sh` channel on `py-backup`. Domain extend: folder archive backup. Public repository: `https://github.com/cloudgen/PyBackup`. Registry is populated — see `index.md`.

`py-backup` follows `requirement-python-cli-default-interaction` (empty argv), `requirement-python-cli-storage` (scratch and persistence), `requirement-python-idempotency` (next archive number), and `requirement-python-sudo-command` (writable first, then `sudo -n`; inner OS-tool sudo stays Gap). The matching `requirement-shell-*` files record the earlier program.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / `APP_NAME` | `PyBackup` |
| Command | `py-backup` |
| Version SSOT | `1.0.0` (`src/PyBackup/__init__.py` and `pyproject.toml`) |
| Ship unit | `src/PyBackup` |
| Public repository | `https://github.com/cloudgen/PyBackup` |
| Install | `python -m pip install --user -e .` from a checkout, or `python -m pip install --user PyBackup` when the package index lists it |
| Backup ops | `requirement-folder-archive-backup` — create / name / deposit / verify / restore |
| Retention total | `requirement-folder-archive-backup-retention-total` — max **30** per basename |
| Retention daily | `requirement-folder-archive-backup-retention-daily` — max **5** per basename per day |
| Domain surface | `requirement-domain-folder-backup` — sole domain SSOT |
| JSON sudoer file | `requirement-sudoer-json-file` — four command objects for `py-backup`; no OS-tool paths |

## Class requirement gate

| Class | Required class file |
|-------|---------------------|
| software-development | `requirement-class-software-dev.md` (**Active**) |
| genesis-template | N/A — this workspace is no longer genesis |

## Purpose

- **Plan** designs work by reading and updating these docs.  
- **Implement** delivers code that **traces** to these requirements.  
- **Review** verifies delivery against requirements and CIAO checklists.

## Layout

| Path | Role |
|------|------|
| `docs/requirements/index.md` | Registry of all requirements — keep in sync |
| `docs/requirements/requirement-*.md` | CIAO-style project requirements |

## Status values

Typical: `draft` · `Active` · `approved` · `in-progress` · `done` · `deprecated` · `superseded`

## Rules

1. Never invent paths — verify on disk.  
2. Class files only via class process; non-class via create-specific process.  
3. Never dump harness inventories into this versioned surface.  
4. Online install requirements stay **absent** unless product mode is explicitly changed.  
5. Sole domain SSOT: `requirement-domain-folder-backup.md`.
