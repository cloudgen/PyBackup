**file**: docs/requirements/requirement-domain-folder-backup.md  
**Status**: Active (Version 1.6.13)  
**Area**: domain  
**Key**: `requirement-domain-folder-backup`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **domain surface Single Source of Truth** for folder-backup: which **specialized CLI verbs** exist, what **help** and **about** must show, and how domain routing is labeled.

**Operational backup behavior** (create, name, deposit, verify, fail-closed matrix) is **not** owned here — it is owned by **`requirement-folder-archive-backup`**.  
**Elevation and sudoers files** (emit / install / submit **workflow**) are owned by **`requirement-three-layer-privilege-model`**.  
**JSON sudoer file body** (grant = **`{{PRJ_NAME}}` only**) is owned by **`requirement-sudoer-json-file`**.

This file remains the sole Active **`requirement-domain-*`** (four pillars).

### 1.1 Human-facing

**In one sentence:** Domain commands are backup, restore, and the grant/draft verbs; this file lists them and what help/about must show — the packing rules live on the backup file.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Type a domain verb | `folder-backup backup /path/to/project` |
| The other role | Help lists work commands apart from grant-emit testers | `folder-backup help` |
| Not this file | How tar/deposit/verify work | `requirement-folder-archive-backup` |

| Includes | Excludes |
|----------|----------|
| Verb catalog, help rows, about fields | A second copy of backup ops |
| Test-purpose grant-emit listed apart | `sudoers` as a typed command |

| Surface | What you open | What for |
|---------|---------------|----------|
| `folder-backup help` | command | listed domain rows |
| `folder-backup about` | command | domain diagnostics |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| See work vs testers | Help has **Work commands** then **Grant and draft setup**. | `folder-backup help` |
| Pack a folder | Ops stay on the backup requirement. | `folder-backup backup /path/to/project` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — Specialized CLI subcommands

| Command | Operands / flags | Handler prefix | Behavior summary | Behavior SSOT |
|---------|------------------|----------------|------------------|---------------|
| `backup` | `<source-folder>` required | `fb_*` | Folder archive backup end-to-end | **`requirement-folder-archive-backup`** |
| `restore` | `<archive\|prefix> [dest]`; flags `--force` `--disk` `--ram` | `fb_*` | Restore archive (default dest: hard-disk host) | **`requirement-folder-archive-backup`** |
| `print-sudoers` | optional output path; `--allow-test-local` when test_local | `fb_*` | Emit **project-sudoers-file** (draft; no `/etc` write) | **`requirement-three-layer-privilege-model`** |
| `print-sudoers-install-script` | optional script path; same trust gate | `fb_*` | Admin handoff script under `/dev/shm` or temp (`install`/`uninstall`/`replace`/`status`) | **`requirement-three-layer-privilege-model`** §2.3.3a |
| `remove-project-sudoers` | optional path; `--force` | `fb_*` | Remove **project-sudoers-file** draft only (not `/etc`) | **`requirement-three-layer-privilege-model`** §2.3.3b |
| `generate-sudoer-request` | optional dest path; `--update` / `--add`; `--allow-test-local` | `fb_*` | Type 0 **independent** generate: write JSON grant to a dest **readable without sudo** (tests/review); compact; both verbs; no `/etc`; no inbound | workflow: **`requirement-three-layer-privilege-model`** §2.3.2a · §2.3.3d · JSON body: **`requirement-sudoer-json-file`** |
| `submit-sudoer-request` | optional sudoers file; `--purpose`; `--update` / `--add`; `--allow-test-local` | `fb_*` | Type 0 submitter: detect sudoer-cli + sudoer-adm + **public inbound**; **default action=update** if this user’s `/etc/sudoers.d/{{APP_NAME}}-<user>` exists, else add; sibling allocates JSON (no `/etc` write; no inbound `mkdir`) | workflow: **`requirement-three-layer-privilege-model`** §2.3.3c · JSON body: **`requirement-sudoer-json-file`** |

**Purpose (this product):** `print-sudoers`, `print-sudoers-install-script`, and `generate-sudoer-request` are **test-purpose**. `backup`, `restore`, `remove-project-sudoers`, and `submit-sudoer-request` are **operational**. Test-purpose verbs stay on `help` under a heading **apart** from operational work and **MUST NOT** appear on any numbered board. All five grant/draft setup verbs **MUST** remain live CLI verbs. Operational `submit-sudoer-request` and `remove-project-sudoers` **MUST** appear on the sudoers board (`requirement-shell-cli-sudoers-submenu`). The three test-purpose verbs stay typed; their numbers stay reserved. **`sudoers` is not a command.**

**Routing:** Dispatcher in `app_main` (CLI interface) **MUST** route these verbs; unknown operands fail closed.

**Non-goals as subcommands:** remote sync, cloud upload, restore UI, schedule daemon (unless a future requirement adds them).

### 2.2 Pillar B — Specialized features (surface map only)

| Feature area | Domain role | Full law |
|--------------|-------------|----------|
| Folder archive backup | Expose `backup` verb | `requirement-folder-archive-backup` |
| Elevated deposit / verify elev | Product uses Type 1 sub-steps | `requirement-three-layer-privilege-model` + backup REQ |
| Sudoers draft print | Expose `print-sudoers` | `requirement-three-layer-privilege-model` |
| Admin sudoers install script | Expose `print-sudoers-install-script` | `requirement-three-layer-privilege-model` §2.3.3a · term `project-sudoers-file` |
| Remove project-sudoers draft | Expose `remove-project-sudoers` | `requirement-three-layer-privilege-model` §2.3.3b |
| Generate sudoer file | Expose `generate-sudoer-request` — **independent** JSON grant to a dest tests/review can read without sudo | workflow: `requirement-three-layer-privilege-model` §2.3.2a · §2.3.3d · body: `requirement-sudoer-json-file` |
| Submit sudoers for approval | Expose `submit-sudoer-request` — JSON request into sibling public inbound | workflow: `requirement-three-layer-privilege-model` §2.3.3c · body: `requirement-sudoer-json-file` |

Domain **MUST NOT** restate full operational backup rules in a second competing SSOT. Pointers and verb catalog only.

### 2.3 Pillar C — Specialized project help items

`help` **MUST** show domain rows (in addition to lifecycle). **Operational** rows and **test-purpose** rows **MUST** be listed **apart** (separate heading). When `APP_LANG=en`, ship unit `app_help` lists work under **Work commands:** and grant-emit testers under **Grant and draft setup (tests and review):** (`requirement-shell-cli-interface` AC-9). Other codes translate those headings and keep the split (`requirement-shell-cli-language`).

**Operational:**

| Help row | Text intent |
|----------|-------------|
| `backup <source-folder>` | Create tar.gz, deposit under backup notation, verify counts |
| `restore <archive\|prefix> [dest]` | Restore archive; default dest **hard-disk** host (reverse ram-drive-first) |
| `remove-project-sudoers [path]` | Delete project-sudoers-file draft only (list/choose if multiple; confirm / `--force`; not `/etc`) |
| `submit-sudoer-request [file]` | Queue a JSON sudoers-grant request via sudoer-cli into `/var/sudoer-cli/sudoer-request` (default **update** if this user’s host fragment exists; `--add`/`--update`; no `/etc` write; no inbound mkdir) |

**Test-purpose** (grant-emit testers; **off every numbered board**; still live CLI verbs):

| Help row | Text intent |
|----------|-------------|
| `print-sudoers` | Emit **project-sudoers-file** (draft) for admin install |
| `print-sudoers-install-script` | Write admin script (`/dev/shm` or temp) for sudo install/uninstall/replace of project-sudoers-file |
| `generate-sudoer-request [path]` | Independently write a JSON grant to a dest tests and review can read (compact; both verbs); no `/etc`; no inbound |

| Help row | Text intent |
|----------|-------------|
| Env note | `BACKUP_*`, `PROJECTS_ROOT`, `RAM_ROOT`, `RESTORE_HOST_DEFAULT` |
| Privilege note | Archive as user; deposit/restore-stage need allowlisted sudo after admin installs fragment |

Examples in help **SHOULD** include:

```text
folder-backup install
folder-backup print-sudoers-install-script
# admin (sudo): sudo sh /dev/shm/folder-backup-<user>-sudoers-admin.sh install
# leave test elev: sudo sh …/…-sudoers-admin.sh uninstall
folder-backup backup /path/to/project
folder-backup generate-sudoer-request
folder-backup submit-sudoer-request ~/.config/folder-backup/sudoer-request-<user>.json
folder-backup submit-sudoer-request
# sibling writes: /var/sudoer-cli/sudoer-request/sudoer-YYYYMMDD-folder-backup-<user>-add-N.json
```

### 2.4 Pillar D — Specialized project about items

`about` **MUST** include domain diagnostics (in addition to Type 0):

| Field / line | Content |
|--------------|---------|
| Backup root | effective `BACKUP_ROOT` |
| Backup notation | effective `BACKUP_NOTATION` |
| Deposit directory | `${BACKUP_ROOT}/${BACKUP_NOTATION}` |
| Sudo deposit status | best-effort probe; honest if not fully probeable |
| sudoer-cli | Detected path or `not_found` |
| sudoer-adm | Detected login or `absent` |
| sudoer inbound | Detected inbound dir or `not_found`; plus writable flag. Preferred: `/var/sudoer-cli/sudoer-request` |
| Host sudoers fragment | `host_sudoers_present` / `host_sudoers_path` — this user’s `/etc/sudoers.d/{{APP_NAME}}-<user>` (or legacy); drives submit default add vs update |
| Domain version note | Product `VERSION` remains Type 0 local version SSOT |

**About is not** a remote version-check. The channel URL in about is Type 0 (`script_url`). Domain rows do not upload archives.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / APP_NAME** | `folder-backup` |
| **Domain prefix** | `fb_` |
| **Ship unit** | `src/folder-backup` |
| **VERSION** | ship unit SSOT (see `src/folder-backup`) |
| **Primary user install** | `~/.local/bin/folder-backup` |
| **Backup operations SSOT** | `requirement-folder-archive-backup` |
| **Privilege / sudoers SSOT** | `requirement-three-layer-privilege-model` (workflow) · `requirement-sudoer-json-file` (JSON grant body) |
| **Submit verb** | `submit-sudoer-request` → `fb_submit_sudoer_request` |
| **Generate verb** | `generate-sudoer-request` → `fb_generate_sudoer_request` |
| **Public inbound (sibling)** | `/var/sudoer-cli/sudoer-request` (3773) |
| **Worked queued basename** | `sudoer-20260815-folder-backup-{{USERNAME}}-add-1.json` |
| **Bootstrap** | Specialized from **selfmanaged**. Channel verbs stay Type 0. Domain stays on this product. |

### 2.5.1 Python ship unit (`py-backup`, current command)

The table above stays the record of `src/folder-backup`. The live Python command does not open a second domain file. Where the two disagree, `py-backup` follows this subsection and `requirement-python-tui`.

| Item | Value |
|------|--------|
| **Product / APP_NAME** | `PyBackup` |
| **Command** | `py-backup` |
| **Domain modules** | `archive`, `sudoers`, `storage` under `src/PyBackup` (no `fb_` prefix) |
| **Ship unit** | `src/PyBackup` |
| **VERSION** | `1.0.0` in `src/PyBackup/__init__.py` and `pyproject.toml` |
| **Install** | `python -m pip install --user` (console script `py-backup`). No `curl` pipe. |
| **Deposit** | `/var/backup/PyBackup` (`BACKUP_ROOT` + `BACKUP_NOTATION`, both overridable) |
| **Detect** | `normal_user_only()` in `src/PyBackup/storage.py` |
| **Menu** | Front **1** client-side, **3** system-log, **4** language, **5** sudoers, **8** self-management, **9** Exit. Client **11**/**12**. Sudoers **52**/**55**. |
| **Bootstrap** | HelloTui architecture. Do not edit HelloTui. Do not reverse-copy. |

Python invocation samples (the CLI requirement names the same tokens):

```text
py-backup backup /path/to/project
py-backup restore alpha --disk
py-backup submit-sudoer-request
py-backup remove-project-sudoers --force
py-backup generate-sudoer-request --allow-test-local
py-backup print-sudoers
py-backup print-sudoers-install-script --allow-test-local
```

`backup` and `restore` steps stay on `requirement-folder-archive-backup`. The JSON body stays on `requirement-sudoer-json-file`.

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Domain surface is explicit (four pillars) and not mixed with full ops law.  
- **Principle 5 – Output SSOT**: Help/about domain rows via product output system.  
- **Principle 9 – Three Types of Commands**: Domain labels Type 0 verbs that invoke Type 1 sub-steps under peer REQs.

---

## Under command line for normal user only

When this program runs on Termux, Git Bash, Windows Command Prompt, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** domain verbs stay listed; backup/restore **MUST** fail closed on that class rather than wrapping `sudo` to deposit.

| MUST | MUST NOT |
|------|----------|
| Help / generate JSON as this login | In-tool `sudo` for domain start/stop |
| Git Bash / Windows cmd: no Termux `pkg` | Treat WSL as this class |

Detect (typical): Termux — `PREFIX` contains `com.termux` or `TERMUX_VERSION` is set. Git Bash — `MSYSTEM` is `MINGW*` / `MSYS*`. Windows cmd — `OS=Windows_NT` and `COMSPEC` names `cmd.exe` after excluding Git Bash, Cygwin, and WSL.

**Implementation Notes:** `src/folder-backup` has **no detect helper yet** (Gap for that file). `src/PyBackup/storage.py` `normal_user_only()` detects Termux, Git Bash, and Windows cmd. `backup()` and `restore()` raise `DomainError` before work on that class and do not wrap `sudo`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent a second backup SSOT in domain.  
- **Intentional:** Pillars A–D only; ops in backup requirement.  
- **Anti-fragile:** Clear ownership boundaries reduce drift.  
- **Over-protect:** Keep sole Active domain file; supersede before replace.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Duplicate full create/name/deposit/verify law here once `requirement-folder-archive-backup` is Active.  
2. Add online install or remote upload as silent domain behavior without new requirements.  
3. Put domain law into bootstrap parent `selfmanaged`.  
4. Leave help listing `backup` without an Active operational backup requirement.  
5. Create a second Active `requirement-domain-*` without superseding this one.  
6. Document inbound as `sudoer-approving` (home dropbox) as the preferred dest.  
7. Let Type 0 `mkdir` `/var/sudoer-cli/sudoer-request`.  
8. Mix test-purpose grant-emit verbs (`print-sudoers`, `print-sudoers-install-script`, `generate-sudoer-request`) into operational help grouping, or put them on any numbered board (they stay typed commands; numbers **51**, **53**, and **54** stay reserved on the sudoers board). The language board is front **7** and does not list those verbs.

**Violating this rule is a critical domain regression.**

Python note (2026-10-22): do not edit HelloTui, and do not copy `py-backup` back onto it. Shell menu numbers in this file stay the record of `src/folder-backup`. The Python menu numbers live in `requirement-python-tui`.

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Four pillars present (subcommands, feature map, help, about) |
| AC-2 | `backup`, `print-sudoers`, `print-sudoers-install-script`, `remove-project-sudoers`, `generate-sudoer-request`, and `submit-sudoer-request` listed with peer SSOT pointers |
| AC-3 | Help lists backup + print-sudoers + install-script + remove-project-sudoers + generate-sudoer-request + submit-sudoer-request; test-purpose grant-emit verbs listed **apart** from operational |
| AC-4 | About lists backup root / notation / deposit dir + sudoer-cli / sudoer-adm / inbound (preferred public path) + `host_sudoers_present` |
| AC-5 | Registered as sole Active domain SSOT |
| AC-6 | No competing full backup ops body (defers to folder-archive-backup) |
| AC-7 | Help/about describe submit as JSON into sibling public inbound, not a home `sudoer-approving` mkdir |
| AC-8 | `print-sudoers`, `print-sudoers-install-script`, and `generate-sudoer-request` are test-purpose on this product; they stay off every numbered board and remain live CLI verbs |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-folder-archive-backup` | **Operational backup SSOT** |
| `requirement-three-layer-privilege-model` | Elevation + sudoers workflow |
| `requirement-sudoer-json-file` | JSON sudoer file body (`{{PRJ_NAME}}` only) |
| `requirement-shell-cli-interface` | Routes domain verbs; help purpose split |
| `requirement-shell-cli-default-interaction` | Numbered boards omit test-purpose grant-emit verbs |
| `requirement-shell-cli-sudoers-submenu` | Operational submit and remove on the sudoers board; test-purpose numbers reserved; all five remain live CLI commands |
| `requirement-bootstrap-chain` | Domain extend from selfmanaged |
| `docs/requirements/index.md` | Registry |

---

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-FOLDER-BACKUP-01,02** | `tests/test_domain_folder_backup.sh` | have | print-sudoers surface (privilege peer) |
| **TP-FOLDER-BACKUP-09** | same | have | about domain fields |
| **TP-CLI-04,06** | `tests/test_cli.sh` | have | help/about list domain verbs |
| **TP-CLI-17** | same | **have** | help lists test-purpose grant-emit verbs apart |
| **TP-FOLDER-BACKUP-19,20** | `tests/test_domain_folder_backup.sh` | have | submit fail-closed / stub inbound (privilege peer) |
| **TP-FOLDER-BACKUP-23,23b** | same | have | host `/etc/sudoers.d` probe → update; `--add` override |
| **TP-FOLDER-BACKUP-24,24b,24c,24d** | same | have | generate-sudoer-request independent dest; suite reads without sudo |
| **TP-FOLDER-BACKUP-21** | same | have | public inbound preferred over leftover `sudoer-approving`; no Type 0 mkdir |
| **TP-FOLDER-BACKUP-21b** | same | have | env inbound override wins over public |
| **TP-FOLDER-BACKUP-22,22b,22c** | same | **have** | JSON sudoer file body — primary: `requirement-sudoer-json-file` |
| **TP-FOLDER-BACKUP-03..08,10** | `tests/test_domain_folder_backup.sh` | have | **Primary map:** `requirement-folder-archive-backup` |

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

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.6.11 | Sudoers board is front **5**. Language board is front **7**. Reserved test-purpose numbers are **51**, **53**, and **54**. | Terminologies section added.
| 2026-10-22 | Active 1.6.12 | Python ship subsection for `py-backup` / `src/PyBackup`. Shell pillars stay. `normal_user_only()` closes the detect Gap for the Python command only. |
| 2026-10-22 | Active 1.6.13 | Python invocation samples for the domain verbs. Shell table stays. |
| 2026-08-03 | Active 1.0.0 | Domain SSOT: folder tar.gz backup + sudoers deposit |
| 2026-08-03 | Active 1.1.0 | Verification rules (later moved to backup ops REQ) |
| 2026-08-03 | Active 1.2.0 | **Thin domain surface**; ops SSOT → `requirement-folder-archive-backup` |
| 2026-08-13 | Active 1.2.0 | Origin notes retarget: specialize from **cli-template** (not selfmanaged) |
| 2026-08-14 | Active 1.3.0 | `submit-sudoer-request` surface |
| 2026-08-15 | Active 1.4.0 | Submit = JSON into `/var/sudoer-cli/sudoer-request`; no inbound mkdir |
| 2026-08-15 | Active 1.4.1 | JSON sudoer file body → `requirement-sudoer-json-file` |
| 2026-08-17 | Active 1.5.0 | Submit default update when this user’s host fragment exists; `--add`/`--update` |
| 2026-08-17 | Active 1.6.0 | `generate-sudoer-request` surface (local verified JSON) |
| 2026-08-17 | Active 1.6.1 | Generate is independent; dest readable for tests/review (three-layer §2.3.2a) |
| 2026-08-23 | Active 1.6.2 | Grant-emit verbs classified test-purpose; help lists them apart; AC-8 |
| 2026-09-03 | Active 1.6.3 | Grant/draft setup verbs stay live CLI commands on the sudoers submenu; not main-menu rows |
| 2026-09-03 | Active 1.6.4 | Submenu SSOT **`requirement-shell-cli-sudoers-submenu`** |
| 2026-09-03 | Active 1.6.5 | Dual mention: submenu membership cites **`requirement-shell-cli-sudoers-submenu`** (start list stays default-interaction) |
| 2026-09-30 | Active 1.6.6 | Origin note is selfmanaged. Domain verbs and the main menu are unchanged. |
| 2026-09-30 | Active 1.6.7 | Test-purpose grant-emit verbs stay off every numbered board. Operational submit and remove stay on the sudoers board. |
| 2026-09-30 | Active 1.6.8 | Reserved sudoers numbers follow the front **7** parent: **71** / **73** / **74**. |
| 2026-09-30 | Active 1.6.9 | Front **6** is the language board. Grant verbs stay off that board. Reserved **71** / **73** / **74** unchanged. |
| 2026-09-30 | Active 1.6.11 | English help headings stay **Work commands:** and **Grant and draft setup (tests and review):**. Other codes translate those headings. |

---

**Last Updated**: 2026-10-22  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
