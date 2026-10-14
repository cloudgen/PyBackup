**file**: docs/requirements/requirement-shell-cli-interface.md  
**Status**: Active (Version 1.13.0)  
**Area**: shell  
**Key**: `requirement-shell-cli-interface`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **project Single Source of Truth** for the **POSIX shell CLI interface** of folder-backup: command surface, privilege typing, global flags, dispatcher behavior, help/about contracts, and mode rules.

It defines a **normal-login** local self-managed shell CLI plus **domain backup** commands and a **narrow elevated deposit** path. Full domain semantics live in `requirement-domain-folder-backup.md`. Full elevation/sudoers rules live in `requirement-three-layer-privilege-model.md`.

### 1.1 Human-facing

**In one sentence:** Type `folder-backup help` to see every live command; work commands and grant-emit testers sit under separate headings; unknown words fail closed.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Type a listed verb | `folder-backup backup /path/to/project` |
| Scripts / CI | `--json` / `--quiet` on a named verb; a pipe with no command places this program | `folder-backup --json version` |
| Not this file | Numbered board membership | `requirement-shell-cli-default-interaction` |

| Includes | Excludes |
|----------|----------|
| Dispatcher tokens, flags, help catalog, channel verbs | Treating local `install` as the pipe |
| Work vs grant-emit headings | `sudoers` as a typed command |

| Surface | What you open | What for |
|---------|---------------|----------|
| `folder-backup help` | command | listed verbs |
| `src/folder-backup` | ship unit | `app_main` |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| See testers apart from work | Help heading **Grant and draft setup** lists print/generate. | `folder-backup help` |
| Type an unknown word | Fail closed. | `folder-backup no-such-command` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Command surface (portable shape)

Every command **MUST** map to exactly one privilege type. Unclassified commands are incomplete design.

| Category | Privilege | Meaning |
|----------|-----------|---------|
| **Type 0 – CLI lifecycle + diagnostics** | Invoking user | `install`, `uninstall`, `where-is-me`, `version`, `about`, `help` |
| **Type 0 – Domain (user work)** | Invoking user | Archive create, naming, staging, sudoers fragment **print** |
| **Type 1 – Narrow elevated deposit** | Controlled sudo (allowlisted only) | Copy staged archive into `/var/backup/...` only |
| **Type 2 – Dedicated system user app ops** | Dedicated app user | **Not in scope** for this product |

### 2.2 Global flags (portable)

| Flag | Env / state | Behavior |
|------|-------------|----------|
| `--quiet`, `-q` | `QUIET=1` | Suppress non-error human output; errors still visible |
| `--json` | `JSON=1` (implies quiet) | Machine-readable structured output |
| `--debug` | `DEBUG=1` | Extra diagnostics on stderr; must not break JSON purity on stdout |
| `--force` | `FORCE=1` / force policy | Skip safe confirms or force reinstall only where documented |

Additional flags **MAY** be added only when documented here (or a superseding requirement) and wired in the dispatcher.

### 2.3 Dispatcher and entry rules

1. **Single entry:** `app_main` **MUST** parse global flags and route commands.  
2. **Unknown command:** **MUST** fail loudly with pointer to `help` (via output SSOT).  
3. **Zero-cli-verb:** interactive → numbered boards (`requirement-shell-cli-default-interaction.md`); non-interactive → `inst_self_install` (`requirement-shell-cli-zero-arguments.md`). **MUST NOT** call `inst_local_install` on that line.  
4. **No raw user I/O:** User-facing messages **MUST** go through `out_*`.  
5. Script end **MUST** call `app_main "$@"` (no basename gate that blocks dispatch).

### 2.4 Help surface

`help` **MUST** list:

- Usage line  
- Every supported command with one-line purpose  
- Privilege category (Type 0 vs elevated deposit)  
- Global flags  
- Honest note that deposit requires admin-installed sudoers fragment  

**Purpose split (orthogonal to Type 0/1):** this product classifies grant-emit verbs as **test-purpose** for help grouping and main-menu exclusion. Help **MUST** list them under a heading **apart** from operational work.

| Purpose | Verbs |
|---------|-------|
| **Operational** | `backup`, `restore`, `remove-project-sudoers`, `submit-sudoer-request`; `menu` / `main` when routed. Grant/draft setup verbs share the **sudoers** family row on the numbered list (`requirement-shell-cli-default-interaction`) |
| **Self-managed** | `install`, `uninstall`, `where-is-me`, `self-install`, `self-update`, `self-uninstall`, `version-check`, `self-management` |
| **Diagnostics** | `version`, `about`, `help` |
| **Test-purpose** | `print-sudoers`, `print-sudoers-install-script`, `generate-sudoer-request` |

Ship unit `app_help` lists operational work under **Work commands:** and grant-emit testers under **Grant and draft setup (tests and review):** when `APP_LANG=en` (AC-9). Other codes translate those headings and keep the same split. Tokens stay Latin.

In JSON mode, help **MUST NOT** dump long human text; return a short structured success/note object.

### 2.5 Implementation Notes (this project)

| Item | Value for folder-backup |
|------|-------------------------|
| **Product / binary name** | `folder-backup` (`APP_NAME`) |
| **Primary executable** | `src/folder-backup` (POSIX `/bin/sh`, single-file ship unit) |
| **Dispatcher** | `app_main` |
| **Output SSOT** | `out_text` + wrappers (`out_info`, `out_success`, `out_warn`, `out_error`, `out_die`, `out_plain`, `out_json`, …) |
| **Version SSOT** | ship unit `VERSION=` in `src/folder-backup` (do not pin a stale number here) |
| **Install paths** | Global: `GLOBAL_BIN` default `/usr/local/bin`; User: `USER_BIN` default `${HOME}/.local/bin` |
| **Primary install story** | User bin: `~/.local/bin/folder-backup` |
| **Online channel env** | **Product UX.** Help lists `SCRIPT_URL`. `install` does not download. A terminal with no command does not download. A pipe with no command does, via `inst_self_install`. |
| **Type 2 commands** | None |
| **Dedicated system user** | Not required |

#### Supported commands (normative for this project)

| Command | Type | Handler family | Required behavior |
|---------|------|----------------|-------------------|
| *(no command — zero-cli-verb)* | Type 0 | interactive `app_cmd_menu`; else `inst_self_install` | Terminal, not quiet, not json: numbered boards. Otherwise CLI self-install. Not local `install`. |
| `install` | Type 0 | `inst_local_install` | Copy running ship unit to privilege-correct bin; mode **0755**; idempotent unless `--force`. **Not** `inst_self_install`. |
| `uninstall` | Type 0 | `inst_local_uninstall` | Remove managed binary; confirm unless `--force` |
| `where-is-me` | Type 0 | `app_where_is_me` | Running + install paths + installed flag |
| `self-install` | Type 0 | `inst_self_install` | Copy when `$0` is a file; download when piped. Local dest mode **0700**, global **0755**. |
| `version-check` | Type 0 | `ver_check` | Compare local `VERSION` with the channel. Needs a reachable `SCRIPT_URL`. |
| `self-update` | Type 0 | `inst_self_update` | Replace the managed binary from the channel. |
| `self-uninstall` | Type 0 | `inst_self_uninstall` | Remove the channel-managed binary. Off-TTY without `--force` fails closed when a binary exists. |
| `self-management` | Type 0 | `app_default_self_loop` → `app_cmd_menu_self` | TTY opens the self board (**61**–**67**). Off a terminal, stops: `self-management needs a terminal`. Front row **6** opens the same board and returns to the front. The argv verb ends after a leaf or Back. |
| `version` | Type 0 | `app_version` | Local `VERSION` only; no network |
| `about` | Type 0 | `app_about` | Diagnostics: install presence, paths, user, shell, TTY, **Cache folder used**, **Cache folder (preferred)**, **Cache folder (1st fallback)**, **Cache folder (2nd fallback)** when this host has one, **Persistence storage** `${HOME}/.local/folder-backup`, channel `script_url`, backup defaults |
| `help` | Type 0 | `app_help` | Full usage in human mode; short JSON note in JSON mode |
| `backup` | Type 0 (+ Type 1 deposit step) | `fb_backup` (domain) | **Operational.** Tar gzip source folder; stage; elevated copy into `/var/backup/${BACKUP_NOTATION}/` |
| `restore` | Type 0 (+ Type 1 stage fetch) | `fb_restore` (domain) | **Operational.** Put an archive back onto the hard-disk projects tree |
| `print-sudoers` | Type 0 | `fb_print_sudoers` (domain) | **Test-purpose.** Emit sudoers fragment for admin to install under `/etc/sudoers.d/` — **does not** write `/etc` itself. Listed apart in help; **off every numbered board**; number **53** stays reserved. Live CLI verb |
| `print-sudoers-install-script` | Type 0 | `fb_print_sudoers_install_script` (domain) | **Test-purpose.** Write admin handoff script under `/dev/shm` or temp — **does not** write `/etc`. Listed apart in help; **off every numbered board**; number **54** stays reserved. Live CLI verb |
| `remove-project-sudoers` | Type 0 | `fb_remove_project_sudoers` (domain) | **Operational.** Remove the local grant draft only (not `/etc`). Sudoers board row **55**. Live CLI verb |
| `generate-sudoer-request` | Type 0 | `fb_generate_sudoer_request` (domain) | **Test-purpose.** **Independent** generate: write JSON grant to a dest tests/review can read without sudo (compact; verify both verbs; sibling convert when present) — **does not** write `/etc` or inbound. Listed apart in help; **off every numbered board**; number **51** stays reserved. Live CLI verb |
| `submit-sudoer-request` | Type 0 | `fb_submit_sudoer_request` (domain) | **Operational.** Detect sudoer-cli + sudoer-adm + public inbound; **update** if this user’s `/etc/sudoers.d` fragment exists else **add**; `--add`/`--update` override — **does not** write `/etc` or `mkdir` inbound. Sudoers board row **52**. Live CLI verb |
| `menu` | Type 0 | `app_cmd_menu` | Numbered boards: front **1** client-side, **7** language, hidden **2**, **5** sudoers, **6** self-management, **9** Exit (`requirement-shell-cli-default-interaction`, `requirement-shell-cli-language`). Same boards as interactive empty argv. Off a terminal, stops: `menu needs a terminal`. **`sudoers` is not a command. `language` is not a command** |
| `main` | Type 0 | `app_cmd_menu` | Alias of `menu`. **MUST NOT** appear as a choice on its own board. |

#### Global flags (normative wiring)

| Flag | Required wiring |
|------|-----------------|
| `--quiet`, `-q` | `QUIET=1` in `app_main` |
| `--json` | `JSON=1` and `QUIET=1` in `app_main` |
| `--debug` | `DEBUG=1` in `app_main` |
| `--force` | `FORCE=1` (and install reinstall policy when applicable) |
| `--update` | `SUBMIT_ACTION=update` + explicit (submit only) |
| `--add` | `SUBMIT_ACTION=add` + explicit (submit only) |

#### Dispatcher acceptance criteria

1. Unknown token after flag parse → `out_die` with pointer to `folder-backup help`.  
2. Zero-cli-verb → interactive numbered boards; non-interactive `inst_self_install` (not local `install`, not help, not backup).  
3. Command routing table in `app_main` **must** include every **Implemented** row above.  
4. Help text **must** stay aligned with that table. Test-purpose verbs **MUST** appear under a heading **apart** from operational verbs.  
5. Domain catalog detail (operands, archive naming, error codes) is owned by `requirement-domain-folder-backup.md` — this file owns the **listed verbs** and routing.

#### Explicitly out of scope

- Calling `inst_local_install` from a zero-cli-verb line
- Type 1 host bootstrap beyond **narrow deposit** and **sudoers fragment generation**  
- Creating the sibling inbound (`sudo sudoer-cli setup` is not this CLI)  
- Type 2 app runtime under a dedicated system user  

### 2.6 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution**: Unknown commands fail loud; force gates destructive ops.  
- **CIAO Principle 2 – Intentional**: Every command has one privilege type and one handler family.  
- **CIAO Principle 5 – Single Source of Output**: Central `out_*`.  
- **CIAO Principle 6 – Single Point of Entry**: `app_main` is the dispatcher SSOT.  
- **CIAO Principle 9 – Three Types of Commands**: Type 0 lifecycle/domain; Type 1 narrow deposit only.  
- **CIAO Principle 10 – Least-Privilege User**: No invented system-user requirement for binary lifecycle.  
- **CIAO Principle 16 – Interactive vs Non-Interactive**: No hang in non-interactive mode.  
- **CIAO Principle 4 / 20 – Over-protect**: Protection Rule blocks privilege and UX regressions.

---

## Under command line for normal user only

When this program runs on Termux, Git Bash, Windows Command Prompt, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** the dispatcher still lists backup/restore; those verbs **MUST** fail closed on that class rather than wrapping `sudo`. Detect lives with privilege/sudo law.

| MUST | MUST NOT |
|------|----------|
| Keep your own login only | Enable in-tool `sudo` because a verb is listed |
| Help remains available | Recommend `sudo curl \| sh` |
| Git Bash / Windows cmd: no Termux `pkg` | Treat WSL as this class |

Detect (typical): Termux — `PREFIX` contains `com.termux` or `TERMUX_VERSION` is set. Git Bash — `MSYSTEM` is `MINGW*` / `MSYS*`. Windows cmd — `OS=Windows_NT` and `COMSPEC` names `cmd.exe` after excluding Git Bash, Cygwin, and WSL.

**Implementation Notes:** ship unit has **no detect helper yet** (Gap).

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Fail loud on bad input; never silent wrong privilege context.  
- **Intentional:** Command table + help + dispatcher stay synchronized.  
- **Anti-fragile:** Works under TTY, quiet, JSON, offline local install.  
- **Over-protect:** Do not collapse Type 0/1, hide the channel verbs, or raw-print user messages.  
- **SSOT:** `APP_NAME` / `VERSION` / flags at config defaults; output via `out_*`; dispatch via `app_main`.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Drop the channel verbs, or point a zero-cli-verb line at `inst_local_install`, without a registry update.  
2. Alias `install` to `self-install`.  
3. List commands in help that are not routed (or route commands not listed).  
4. Bypass `out_*` for product user messages.  
5. Run the entire CLI as root by default instead of narrow deposit elevation.  
6. Put full domain archive semantics only here and omit the domain SSOT.  
7. Add a second submit verb (`submit-sudoer`) without routing + help, or invent inbound `mkdir` as this CLI’s job.  
8. Route a non-interactive zero-cli-verb to help, or drop `menu`/`main` routing.  
9. Mix test-purpose verbs (`print-sudoers`, `print-sudoers-install-script`, `generate-sudoer-request`) into operational help grouping, or put them on any numbered board (they stay typed commands and help rows; numbers **51**, **53**, and **54** stay reserved).  
10. Wire `sudoers` as a live dispatcher token, or drop a grant/draft setup verb from the dispatcher.

**Violating this rule is a critical CLI interface regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | All **Implemented** commands in the table are routed and listed in help |
| AC-2 | Global flags wire QUIET/JSON/DEBUG/FORCE as specified |
| AC-3 | Interactive zero-cli-verb is the numbered boards; non-interactive zero-cli-verb is `inst_self_install`; never local `install` |
| AC-4 | Channel verbs are routed and listed in help; they are self-board rows **64**–**67** (and `self-management` opens that board), not front rows |
| AC-5 | Domain verbs point to domain requirement for deep semantics |
| AC-6 | `submit-sudoer-request` is Type 0, routed, listed in help; does not write `/etc` or create inbound |
| AC-7 | `generate-sudoer-request` is Type 0, routed, listed in help; independent of submit; dest is invoking-user readable; does not write `/etc` or inbound |
| AC-8 | `menu` and `main` are routed and listed in help; interactive empty argv opens the same boards (`requirement-shell-cli-default-interaction`) |
| AC-9 | Help lists test-purpose `print-sudoers`, `print-sudoers-install-script`, and `generate-sudoer-request` **apart** from operational verbs; those three are **not** on any numbered board. English headings `Work commands:` and `Grant and draft setup (tests and review):` stay exact. Other codes translate the headings and keep the split. **have** |
| AC-10 | Five grant/draft setup verbs remain routed live CLI commands; operational submit and remove are sudoers rows **52** and **55**; `sudoers` is **not** a dispatcher token |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-shell-cli-zero-arguments` | **Active** — non-interactive zero-cli-verb is `inst_self_install` |
| `requirement-shell-cli-default-interaction` | Case 2 empty argv + claimed `menu`/`main` numbered boards |
| `requirement-shell-cli-sudoers-submenu` | Front **5** sudoers board; **52**/**55** printed; test-purpose reserved; `sudoers` not dispatched |
| `requirement-shell-local-self-management` | install/uninstall/where-is-me |
| `requirement-shell-output-requirements` | `out_*` catalog |
| `requirement-domain-folder-backup` | Domain four pillars |
| `requirement-three-layer-privilege-model` | Elevation model |
| `docs/requirements/index.md` | Registry |

---

## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-01..12** | `tests/test_cli.sh` | have |
| **TP-CLI-13..16** | same | **have** — `menu`/`main` (`requirement-shell-cli-default-interaction`) |
| **TP-CLI-17** | same | **have** — help lists test-purpose grant-emit verbs apart (AC-9) |

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
| 2026-10-14 | Active 1.13.0 | Family sudoers is front **5** and is not dispatched. Front **7** language is not dispatched. Self board is front **6**, rows **61**–**67**. | Terminologies section added.
| 2026-08-03 | Active 1.0.0 | CLI surface for local-only folder-backup + domain backup |
| 2026-08-15 | Active 1.1.0 | `submit-sudoer-request` listed as Type 0 JSON submit into sibling public inbound |
| 2026-08-17 | Active 1.2.0 | `--add` / `--update`; default submit action from host `/etc/sudoers.d` probe |
| 2026-08-17 | Active 1.3.0 | `generate-sudoer-request` Type 0; AC-7 |
| 2026-08-17 | Active 1.3.1 | Generate dest must be readable for tests/review; independent of submit |
| 2026-08-23 | Active 1.4.0 | `menu` / `main` listed (Gap); empty argv stays help |
| 2026-08-23 | Active 1.5.0 | Restore / print-sudoers-install-script / remove-project-sudoers listed; test-purpose grant-emit verbs apart in help (AC-9) |
| 2026-08-23 | Active 1.6.0 | `menu` / `main` routed (`app_main_menu`); empty argv stays help |
| 2026-08-28 | Active 1.7.0 | Case 2: TTY empty argv = numbered list; off-TTY help; zero-arguments Withdrawn |
| 2026-09-03 | Active 1.8.0 | Grant/draft setup verbs stay live CLI commands; numbered **main** list uses family **sudoers** (submenu); `sudoers` not dispatched; AC-10 |
| 2026-09-03 | Active 1.8.1 | Submenu SSOT **`requirement-shell-cli-sudoers-submenu`** |
| 2026-09-06 | Active 1.8.2 | §1.1 Human-facing; help **Work commands** vs **Grant and draft setup** (AC-9 / TP-CLI-17 have); Under command line section |
| 2026-09-27 | Active 1.8.3 | About cache lines: used, preferred, 1st fallback, 2nd fallback when this host has one (`requirement-shell-cli-storage` 1.4.0) |
| 2026-09-30 | Active 1.9.0 | Channel verbs from selfmanaged are routed. `install` stays the local copy. Main menu unchanged. |
| 2026-09-30 | Active 1.9.1 | Handlers `app_cmd_menu` / `app_cmd_menu_self`. Self board **81**–**87**. Test-purpose verbs off every numbered board. Sudoers rows **172** and **175**. |
| 2026-09-30 | Active 1.10.0 | Non-interactive zero-cli-verb is `inst_self_install`. Interactive zero-cli-verb stays the boards. Local `install` stays `inst_local_install`. |
| 2026-09-30 | Active 1.10.1 | Named `menu` and `self-management` off a terminal stop. They do not print help. |
| 2026-09-30 | Active 1.11.0 | Sudoers board is front **7**. Printed rows **72** and **75**. Reserved **71** / **73** / **74**. |
| 2026-09-30 | Active 1.12.0 | Front **6** is language. `language` is not dispatched. |
| 2026-09-30 | Active 1.13.0 | English help headings in AC-9 stay exact. Other codes translate those headings and keep the split. |

---

**Last Updated**: 2026-10-14  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
