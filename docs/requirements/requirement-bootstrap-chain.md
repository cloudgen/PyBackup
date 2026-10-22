**file**: docs/requirements/requirement-bootstrap-chain.md  
**Status**: Active (Version 2.5.0)  
**Area**: architecture  
**Key**: `requirement-bootstrap-chain`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare the **bootstrap chain** for this product: ordered lineage, direction, architecture inheritance, and the **domain extend** of folder-archive backup onto the parent CLI you install for yourself.

**Direction is sacred:** ancestor → descendant only. Never reverse-copy this product onto the bootstrap parent.

### 1.1 Human-facing

**In one sentence:** folder-backup is rebuilt from the sibling **selfmanaged** CLI; copy architecture **from** that parent **to** this product, never the reverse.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Work in this tree (`src/folder-backup`) | `sh src/folder-backup version` |
| The parent | Sibling `selfmanaged` — self-install, version-check, self-update, self-uninstall | Keep that tree as the origin |
| Not this file | Backup/restore verbs, sudoers grant body | `requirement-domain-folder-backup` |

| Includes | Excludes |
|----------|----------|
| Ancestor → descendant only | Copying this product onto selfmanaged “to share fixes” |
| Parent channel verbs kept, plus this product’s local `install` | Calling local `install` from a pipe with no command |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/folder-backup` | this product | live ship unit |
| `docs/requirements/index.md` | registry | lineage row |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Change this product | Edits stay here. Do not overwrite the parent CLI. | work under this workspace root |
| Check install mode | A terminal with no command is the numbered boards. A pipe with no command is `self-install`. | `curl … \| sh` places this program |

---

## 2. Core Rules (Mandatory)

### 2.1 Direction

1. Every edge **MUST** be **ancestor → descendant** only.  
2. Plans **MUST NOT** copy this product’s ship unit onto the bootstrap parent to “share fixes.”  
3. Detected reverse-copy **MUST** be treated as critical pollution (restore parent; rebuild this product).

### 2.2 Chain declaration (this product)

| Field | Value |
|-------|--------|
| **Root / hop 0 (A)** | `selfmanaged` — Type 0 self-managed CLI with channel verbs (sibling workspace `{{PROJECTS_ROOT}}/selfmanaged`) |
| **Leaf / hop 1 (B)** | `folder-backup` — this workspace product |
| **Immediate origin of leaf** | `selfmanaged` |
| **Specialize mode** | **Domain extend** (folder archive backup + sudoers-elevated deposit) **and keep** A’s channel verbs. Not a trim. |
| **A ship unit** | Sibling: `{{PROJECTS_ROOT}}/selfmanaged/src/selfmanaged` (not in this tree; do not write it from here) |
| **B ship unit** | `src/folder-backup` |
| **A channel ownership** | `self-install`, `version-check`, `self-update`, `self-uninstall`; composed `SCRIPT_URL` |
| **B channel ownership** | Same verbs, retargeted to `REPO_USER` / `REPO_NAME` = this product. A non-interactive zero-cli-verb is `inst_self_install` (CLI place), not local `install`. |
| **A domain** | none (Type 0 lifecycle) |
| **B domain** | folder tar.gz backup + sudoers-elevated deposit (see `requirement-domain-folder-backup`) |
| **Retired names (not live hops)** | `cli-template` — live parent from 2026-08-13 through 2026-09-29. **Not** the live parent after 2.2.0. |

### 2.3 Architecture inheritance (B from A)

B **MUST** inherit A’s structural contracts:

| Layer | Inherit / extend |
|-------|------------------|
| Runtime | POSIX `/bin/sh`, `set -u`, explicit errors |
| Output SSOT | `out_*` family |
| Modular prefixes | `out_`, `inst_`, `util_`, `app_`, `path_`, `prompt_`; domain uses dedicated `fb_` prefix |
| Entry / dispatch | Single `app_main`; always call `app_main "$@"` at end |
| Global flags | `--quiet` / `--json` / `--debug` / `--force` / `--global` |
| Integrity companion | **Keep** A’s `CHECKSUM` download check when set. No separate checksum requirement file. |
| Online lifecycle | **Keep** `self-install`, `version-check`, `self-update`, `self-uninstall`, `self-management` |
| Local lifecycle | **Keep** folder-backup `install` / `uninstall` / `where-is-me` (`inst_local_*`, mode **0755**) |
| Empty argv | **Extend** interactive boards / non-interactive `inst_self_install` |
| Domain | **Add** on B only |

### 2.4 Keep / extend matrix (normative for this product)

| Surface | Decision | Notes for folder-backup |
|---------|----------|-------------------------|
| `out_*` output SSOT | **Keep** | Surgical only |
| Modular single-file design | **Keep** | Ship unit under `src/` |
| Global flags + `app_main` | **Keep** | Same contracts; domain flags added on B |
| Storage resolve | **Keep / adapt** | Staging for tar.gz |
| Idempotency / interactive modes | **Keep / retarget** | Domain confirm paths stay fail-closed |
| Online channel (`SCRIPT_URL`, `REPO_*`) | **Keep** | Composed for this product. Help lists the URL. `install` does not download. |
| Non-interactive zero-cli-verb | **Take as CLI self-install** | `inst_self_install` (copy or download). Not local `install`. Interactive line stays the boards |
| `self-install` / `version-check` / `self-update` / `self-uninstall` | **Keep** | Explicit verbs. `self-install` is `inst_self_install` (script copy or download). |
| `self-management` | **Keep** | TTY opens the self board (front row **6**, rows **61**–**67**). Off-TTY help. |
| Companion `CHECKSUM` | **Keep code path** | Optional env. Not a second requirement file. |
| Local `install` / `uninstall` / `where-is-me` | **Keep** | `install` stays `inst_local_install` (mode **0755**). Do not alias it to `self-install`. |
| Domain backup + sudoers fragment | **Add** | Domain SSOT |
| Domain / out Protection Zones | **Keep spirit** | Do not “simplify away” defensive layers for style |

### 2.5 Identity retarget (B only)

| Concern | B value |
|---------|---------|
| `APP_NAME` | `folder-backup` |
| `VERSION` | ship unit SSOT (see `src/folder-backup`; do not pin a stale number here) |
| Primary day-to-day install | Local copy `install` → `${USER_BIN}` (default `~/.local/bin`), mode **0755** |
| Channel place | `self-install` / `self-update`, and a non-interactive zero-cli-verb (copy when `$0` is a file; download when piped) |
| README | The pipe one-liner is the online install. Local `install` stays the checkout copy |

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **A (bootstrap)** | `selfmanaged` at `{{PROJECTS_ROOT}}/selfmanaged` (do not reverse-copy; do not edit A from this tree) |
| **B (this product)** | folder-backup |
| **Specialize intent** | A’s architecture and channel verbs, plus folder-backup domain and the folder-backup main menu |
| **Install mode** | **Dual.** `install` copies the running file (mode 0755) and is self-board row **61**. `self-install` is the channel verb (row **67**) and the non-interactive zero-cli-verb. A terminal with no command is the numbered boards. |
| **Cache host knob** | `SELFMANAGED_CACHE_HOST` stays that name (inherited). Do not rename it. |
| **Domain after specialize** | Active `requirement-domain-folder-backup` |
| **Historical origin** | 2026-08-03 first named `selfmanaged` then trimmed online. 2026-08-13 retargeted A to `cli-template` and dropped the channel. 2026-09-30 user ordered A=`selfmanaged` again and **kept** the channel. |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Lineage and domain extend are explicit.  
- **Principle 1 – Caution**: Channel verbs are explicit. Empty argv does not download.  
- **Principle 18 / Over-protect**: Reverse-copy is forbidden pollution.  
- **Principle 21 – Dual policies**: Complete B law; portable cores elsewhere.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Matrix before delete; verify no half-live install.  
- **Intentional**: Explicit keep/extend; the registry names the live parent.  
- **Anti-fragile**: Keep battle-tested `out_*` / modular patterns from A.  
- **Over-protect**: Never reverse-copy; do not hide the channel or alias `install` to it.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Reverse-copy `folder-backup` onto `selfmanaged` or treat reverse as “cleanup.”  
2. Name `cli-template` as this product’s live origin without updating this file.  
3. Point a zero-cli-verb line at `inst_local_install`, or print help for a pipe with no command.  
4. Alias `install` to `inst_self_install`, or drop `self-install` while claiming A’s lifecycle.  
5. Drop `out_*` / modular Protection Zones as “part of specialize.”  
6. Invent a second bootstrap origin that contradicts this declaration without updating this file.  
7. Rename `SELFMANAGED_CACHE_HOST`.

**Violating this rule is a critical bootstrap-direction regression.**

Python note (2026-10-22): do not reverse-copy `PyBackup` onto HelloTui. Do not treat the shell channel in §2.4 as the install path of `py-backup`. That command uses `python -m pip` (`requirement-python-cli-interface`).

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Hop table names A=selfmanaged, B=folder-backup, direction A→B |
| AC-2 | Keep/extend matrix matches the registry (channel verbs kept; domain present; interactive boards / non-interactive self-install) |
| AC-3 | B identity retarget complete (`APP_NAME=folder-backup`, `VERSION` matches the ship unit hard-assign, this product’s `SCRIPT_URL`) |
| AC-4 | Domain SSOT present for backup surface |
| AC-5 | `install` is local copy mode 0755; `self-install` is the channel verb |
| AC-6 | The Python command follows §6b (HelloTui → PyBackup, pip, empty off-terminal is help). AC-1 through AC-5 stay the record of `src/folder-backup` |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-class-software-dev` | Class gate |
| `requirement-shell-local-self-management` | Local `install` / `uninstall` / `where-is-me` (not the channel verbs) |
| `requirement-shell-cli-zero-arguments` | **Active** — non-interactive zero-cli-verb is `inst_self_install` |
| `requirement-shell-cli-default-interaction` | Interactive zero-cli-verb numbered boards |
| `requirement-domain-folder-backup` | Domain extend |
| `docs/requirements/index.md` | Registry |

---

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-CLI-04,10** | `tests/test_cli.sh` | have | help lists channel verbs; offline `version-check` / `self-update` fail closed |
| **TP-CLI-07** | `tests/test_cli.sh` | have | Off-TTY empty argv is CLI self-install |
| **TP-CLI-13** | `tests/test_cli.sh` | have | TTY empty argv numbered boards (case 2) |
| **TP-FOLDER-BACKUP-*** | `tests/test_domain_folder_backup.sh` | have | domain extend |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`

## Terminologies

Copied substance for the words this requirement uses.

### CLI main menu numbering

**Definition:** CLI main menu numbering is the portable rule set for integers on a claimed CLI default interaction tree. A command number is unique in the whole tree: a child list must not reuse 1, 2, or 6, or any other parent token. A child command number must start with its parent's number as prefix: 11… under 1, 21… under 2, 51… under 5 when a sudoers family is claimed, 61… under 6, 71… under 7 when a language board is claimed, and 111… under 11. The front board uses small category integers plus Exit 9. Every submenu and data picker uses 0 to go back to the parent list. This term owns which integers, not ink and not the catalog of rows.

**Human daily-life explanation:** CLI main menu numbering is how the café numbers dishes so 11 always means the same plate, even after you walk into a side room. The side-room specials do not start again at 1. They keep the front number as a prefix (11, 111). 0 is the door back to the previous board. 9 on the front board is leaving the café.

**Daily-life example:** Front board 1, client side, opens a second board whose first dish is 11, not another 1. If the kitchen reused 1, nobody would know whether you meant the front door or the first side dish.

### Well-known menu

**Definition:** A well-known menu is the portable numbered TTY membership of well-known CLI verbs, plus the category front rows and front Exit, shared across self-managed products that claim a CLI default interaction. It is the portable subset of a CLI main menu hierarchy table: front board 1 / 2 / 5 / 6 / 7 / 9 and self-management 61…67 under 6. Those integers stay reserved. Which rows a product prints follows the language consider table (shell column versus Python / pip column). Domain numbered rows belong on the full hierarchy table, not this catalog.

**Human daily-life explanation:** A well-known menu is the shared café numbering every similar kitchen agrees on. The front chalkboard has rooms 1, 2, 5 when a sudoers family is claimed, 6 for self-care, and 7 when a language board is claimed, plus 9 to leave. The back-office list under 6 keeps the same dish numbers.

**Daily-life example:** You walk into a shell shop in the family. 6 is self-care. 67 files this tool in the drawer. 61 stocks the pantry when that shop sells extra kits. You walk into a pip shop: 6 is still self-care, 64 and 65 ask the package counter to compare and refresh, and 61 is not "pip install this program."

## 6b. Python chain (`py-backup`, user order 2026-10-22)

Sections 2.1 through 2.6 still describe `src/folder-backup` and the selfmanaged channel. They stay. The live Python command is a second hop. It does not delete that shell chain.

| Item | Value |
|------|--------|
| **A** | HelloTui (sibling workspace). Do not edit A. Do not reverse-copy B onto A. |
| **B** | PyBackup. Command `py-backup`. Ship unit `src/PyBackup`. Version `1.0.0`. |
| **Channel** | `python -m pip`. No `SCRIPT_URL`. No `curl` pipe. |
| **Empty argv** | A terminal opens the text menu. No terminal prints help and returns 0. Not `self-install`. |
| **Front rows** | **1** client-side, **3** system-log, **4** language, **5** sudoers, **8** self-management, **9** Exit. Row **2** stays omitted. |
| **Self rows** | **82** version, **83** about, **84** version-check, **85** self-update, **86** self-uninstall, **87** self-install |
| **Domain** | `requirement-domain-folder-backup` §2.5.1 and `requirement-python-tui` |
| **Shell file** | `src/folder-backup` release 1.26.0 remains the behavioral record of the channel chain |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 2.4.0 | Self board is front row **6**, rows **61**–**67**. `install` is row **61**. `self-install` is row **67**. | Terminologies section added.
| 2026-08-03 | Active 1.0.0 | Declared A=selfmanaged → B=folder-backup (trim online) |
| 2026-08-13 | Active 2.0.0 | Re-specialize: A=cli-template → B=folder-backup (domain extend). selfmanaged retired. |
| 2026-08-28 | Active 2.1.0 | Empty argv **extend**: case 2 TTY menu; Type O still absent |
| 2026-09-30 | Active 2.2.0 | User ordered A=`selfmanaged` again. Channel verbs kept. Empty argv stays case 2. `install` stays the local copy. |
| 2026-09-30 | Active 2.2.1 | Self board is front row **8**. Empty argv wording is numbered boards. Version cell and AC-3 point at the ship unit. |
| 2026-09-30 | Active 2.4.0 | Non-interactive zero-cli-verb is `inst_self_install`. Interactive line stays the boards. Local `install` stays the 0755 copy. |
| 2026-10-22 | Active 2.5.0 | Python chain §6b: A=HelloTui → B=PyBackup. Pip, not the shell channel. Empty argv off a terminal is help. Shell AC-1 through AC-5 unchanged. |

---

**Last Updated**: 2026-10-22  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
