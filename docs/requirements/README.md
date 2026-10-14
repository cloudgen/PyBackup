# Requirements

Authoritative specialized product law for **folder-backup** lives here.

**Current state (2026-10-14):** Specialized **software-development** product. Left genesis. Bootstrap parent is sibling **selfmanaged**. Channel verbs stay (`self-install`, `version-check`, `self-update`, `self-uninstall`). A terminal with no command is the numbered boards. Front rows are client-side **1**, sudoers **5**, self-management **6**, language **7**, and Exit **9**. A pipe with no command is `self-install`. Domain extend: folder archive backup. Eight OS family labels cite sibling tn5250-cli and do not add a compiler install. Registry is populated — see `index.md`.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / `APP_NAME` | `folder-backup` |
| Version SSOT | `1.26.0` (ship unit hard-assign) |
| Ship unit | `src/folder-backup` |
| Default install | `~/.local/bin/folder-backup` |
| Install mode | **Dual.** `install` copies this file (mode `0755`). A pipe with no command, and `self-install`, place the CLI (local `0700`, global `0755`). A terminal with no command is the boards. |
| Backup ops | `requirement-folder-archive-backup` — create / name / deposit / verify / restore |
| Retention total | `requirement-folder-archive-backup-retention-total` — max **30** per basename |
| Retention daily | `requirement-folder-archive-backup-retention-daily` — max **5** per basename per day |
| Domain surface | `requirement-domain-folder-backup` — four pillars; ops deferred |
| JSON sudoer file | `requirement-sudoer-json-file` — grant is `folder-backup` only; no `cp`/`mkdir` |

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
