**file**: docs/requirements/requirement-shell-cli-default-interaction.md  
**Status**: Active (Version 1.13.0)  
**Area**: shell  
**Key**: `requirement-shell-cli-default-interaction`  
**Optional RQ-ID**: `RQ-SHELL-CLI-DEFAULT-INTERACTION`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file records the shell menu. The live command `py-backup` follows `requirement-python-cli-default-interaction`.

This requirement is the shell record for folder-backup’s **claimed default interactive main menu**.

Channel verbs exist (`self-install`, `version-check`, `self-update`, `self-uninstall`, `self-management`). **Case 2** applies to the **interactive** zero-cli-verb: on a real terminal, with quiet and json off, a bare `folder-backup` run opens the numbered boards. A **non-interactive** zero-cli-verb (no TTY, or `--quiet` / `--json` with no command) is CLI self-install, owned by **`requirement-shell-cli-zero-arguments`**. This file does not replace that path. Named commands **`menu`** and **`main`** open the same boards. Off a terminal those named commands stop: `menu needs a terminal`. The sudoers **board body** is owned by **`requirement-shell-cli-sudoers-submenu`**. **`sudoers` is not a live dispatcher token.**

### 1.1 Human-facing

**In one sentence:** At a real terminal, type `folder-backup` with no command to see numbered boards — client-side, sudoers, self-management, language, and Exit — with server-side hidden; pick **7** for the display language and **5** for grant and drafts. A pipe with no command places this program (`requirement-shell-cli-zero-arguments`). Naming `menu` off a terminal stops.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Open the boards or pick a number | `folder-backup` then `1` |
| The other role | Scripts and CI must not hang on those boards | `folder-backup </dev/null` → help |
| Not this file | Full command catalog, flags, unknown tokens | `requirement-shell-cli-interface` |

| Includes | Excludes |
|----------|----------|
| Front rows **1** client-side, **5** sudoers, **6** self-management, **7** language, **9** Exit | A printed server-side row |
| One hide sentence before the numbers: server-side stays reserved | An empty server loop |
| Client rows **11** backup, **12** restore, **0** Back | Restarting a child board at **1** |
| Self rows **61**–**67** and **0** Back | `help`, `menu`, or `main` as a choice |
| Sudoers board body (owned next door) | A live `sudoers` CLI command |
| Bare run on a real terminal | Install-ensure on empty argv |
| `menu` / `main` as the same boards | Test-purpose grant-emit verbs on any numbered board |

| Surface | What you open | What for |
|---------|---------------|----------|
| `./src/folder-backup` | ship unit | live dispatch (empty argv, `menu`, `main`) |
| `folder-backup help` | command | listed verbs including lifecycle |
| `folder-backup` | empty argv | numbered boards on a real terminal |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the boards at a prompt | The program prints **folder-backup**(*live version*) then the front board. On a real terminal the name is bold, the version italic, each short name is bold, and each “what it does” line after the colon is italic and light gray. `--json` on `menu`/`main` is ignored on a real terminal. | `folder-backup` or `folder-backup menu` |
| Pack a folder | Client row **11**, then the folder (one field at a time) or read Next. A finished pick returns to the front board. | `1` then `11` then a source folder path |
| Put an archive back | Client row **12**. | `1` then `12` |
| Choose the menu language | Front row **7** opens **71**–**78**. The choice is kept for this login. | `7` then `72` |
| Set up a grant or draft | Front row **5** opens the sudoers board. Operational rows only. Test commands stay typed. | `5` |
| Install, version, or update this program | Front row **6**. Local copy is **61**. Channel place is **67**. | `6` then `61` |
| Step back one board | Back on a child board | `0` |
| Leave the menu | Exit on the front board | `9` |
| Run a bare invocation in CI | No prompt. The program places itself. | `folder-backup </dev/null` |
| Name the menu in a script | The program stops. The next step is help. | `folder-backup menu </dev/null` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Claim and case

1. This product **claims** a default interactive main menu.  
2. **Case 2** applies to the **interactive** zero-cli-verb. The non-interactive zero-cli-verb is **`requirement-shell-cli-zero-arguments`** (`inst_self_install`).  
3. This file **owns the numbered boards**. It does not own a pipe with no command.  
4. An interactive zero-cli-verb (`TTY=1`, `JSON=0`, `QUIET=0`, no verb after switches) **MUST** open the numbered boards (`app_cmd_menu`). It **MUST NOT** place the program.  
5. A non-interactive zero-cli-verb **MUST NOT** draw these boards and **MUST NOT** be help. That route is `inst_self_install`.  
6. `--json` or `--quiet` with **no command token** is a non-interactive zero-cli-verb (self-install), including on a terminal.  
7. Routed-verbs **`menu`** and **`main` MUST** call the same handler. They remain valid ways to open the boards.  
8. `app_main` **MUST** route `menu` / `main` to `app_cmd_menu`. `app_main_menu` **MAY** remain a one-line alias of `app_cmd_menu`.  
9. `requirement-shell-cli-zero-arguments` **MUST** stay **Active** and own the non-interactive zero-cli-verb.

### 2.2 Mode check

Measure interactive capability **outside functions** (`TTY=1` only when stdin and stdout are terminals). Helpers consume `TTY` (`requirement-shell-interactive-vs-noninteractive`).

| Invocation | Mode | `--json` | MUST | MUST NOT |
|------------|------|----------|------|----------|
| `folder-backup` (no command) | Interactive (`TTY=1`, not quiet, not json) | off | Draw the numbered boards | Help; hang; place |
| `folder-backup` (no command) | Non-interactive (`TTY=0`, or quiet, or json) | follows the switch | **CLI self-install** (`requirement-shell-cli-zero-arguments`) | Draw the menu; hang; help |
| Flags only, no command (`--debug` / `--force`) | Interactive | off | Draw the numbered boards | Place; help |
| Flags only, no command (`--quiet` / `--json`) | Any | on | CLI self-install | Draw the menu; JSON help |
| `folder-backup menu` or `main` | Interactive (`TTY=1`) | **Ignore** | Draw the numbered boards | Treat as JSON help; hang |
| same | Non-interactive (`TTY=0`) | error when JSON=1 | **Stop**: `menu needs a terminal. Next: folder-backup help` (exit 1; JSON error when JSON=1) | Draw the menu; hang; print help; exit 0 |
| `folder-backup self-management` | Interactive (`TTY=1`) | **Ignore** while drawing | Draw the self board only (§2.3.3) | Draw the front board; hang |
| same | Non-interactive (`TTY=0`) | error when JSON=1 | **Stop**: `self-management needs a terminal. Next: folder-backup help` | Draw the self board; hang; print help |

While a board is **drawing**, saved `JSON` and `QUIET` **MUST** be forced off, then restored before a leaf runs. That force applies only when `TTY=1`. Named `menu` / `main` / `self-management` off a terminal **MUST** `out_die`. A zero-cli-verb `--quiet` or `--json` is self-install, not that stop. Interactive `menu --json` still draws.

### 2.3 Boards

0. **Look (mandatory):** every numbered board **MUST** use the default CLI main menu style. Header **MUST** print live `folder-backup(VERSION)` (no space; same Config scalars as `version`) then the board title. On a TTY the name is **bold** and the version *italic*. Each numbered short name **MUST** be **bold** (SGR **1**). Each numbered `explain` **MUST** be *italic* and light gray (SGR **3** + **37**). The number stays unstyled. **Exit** and **Back** have no explain and stay unstyled. Off-TTY / JSON: **plain** — **MUST NOT** emit CSI. Typical helpers: `util_app_ident` then `out_menu_choice`. **MUST NOT** a bare `folder-backup` on that header. **MUST NOT** print `explain` unstyled on a TTY. **MUST NOT** print the short name unstyled on a TTY.  
1. The front board title **MUST** be `numbered list`.  
2. **Parent-prefix integers.** Child boards **MUST NOT** restart at **1**. Hidden numbers **MUST NOT** be compacted.  
3. Printed command-row text **MUST** be `{{short-descript}}: {{explain}}`. Routed leaves use the kept-list human-readable explain. Category rows (`client-side`, `self-management`, family `sudoers`) use this file’s table.  
4. A choice **MUST** be read in the **current shell**. On a numbered board: `out_msg_n` of the language choose-prompt, then `read -r _prompt_line`. **MUST NOT** pass that prompt through `prompt_line` (that helper appends another colon). Field prompts stay `prompt_line`. **MUST NOT** `_pick=$(prompt_line …)` / `_pick=$(prompt_ask …)` / `$()` / backticks of **any** function whose body contains `read` (do-not-capture-read / **PP-A-22**). stderr+$() is **not** a license. Menu copy follows `APP_LANG` (`requirement-shell-cli-language`). English text in this file is the `en` catalog.  
5. An invalid choice **MUST** use `out_error` (not `out_die`, not `out_warn`) and **MUST** reprint **this** layer.  
6. **0** / `back` / `Back` / empty line / EOF on a **child** board is **Back** to the parent. `exit` / `quit` on a child board is the same Back. Child boards **MUST NOT** print Exit **9** and **MUST NOT** print Back as a front-row number.  
7. Front Exit is **9**, **99**, `exit`, `quit`, `q`, an empty line, or EOF, and returns 0. `q` on a **child** board is Back.  
8. After a valid leaf opened from the front (or from a child of the front), the front board **MUST** redisplay. **MUST NOT** exit the menu on success. **MUST NOT** stay on the launching child board. A leaf that calls `out_die` still ends the process. An empty required backup/restore field prints `Next:` and the front redisplays.  
9. Typing a **listed leaf verb** at the front pick prompt **MUST** run that leaf, then redisplay the front. Typing `sudoers` or **5** at the front **MUST** open the sudoers board. Typing `sudoers` at the client **MUST** be an invalid choice. Typing a child number on the wrong layer **MUST** be invalid.  
10. **`sudoers` is not a live CLI command.** `folder-backup sudoers` **MUST** remain unknown.

#### 2.3.1 Front board

Print the hide sentence **before** the numbers, then the rows below. Row **2** is **not** printed. Typing **2** is an invalid-choice retry. **MUST NOT** add `app_cmd_menu_server`.

Hide sentence (exact): `server-side is not available: this program does not run a host service. Number 2 stays reserved.`

| # | Token | Label |
|---|-------|-------|
| *(header)* | — | `**folder-backup**(*VERSION*) — numbered list` |
| *(hide)* | — | server-side sentence above |
| 1 | category `client-side` | `client-side: this login's folders: pack and restore` |
| 5 | family `sudoers` | `sudoers: Grant and drafts` |
| 6 | category `self-management` | `self-management: this CLI install, version, update, uninstall` |
| 7 | category `language` | `language: display language for this menu` |
| **9** | **Exit** | leave the menu |

Front rows **MUST NOT** be `help`, `menu`, `main`, `uninstall`, `where-is-me`, `backup`, `restore`, the five grant/draft verbs, or a test-purpose verb. Channel verbs and diagnostics are board **6**, not front rows. The family row **5** is the grant board, not those five verbs. Row **7** opens the language board (`requirement-shell-cli-language`). Invalid front text when `APP_LANG=en`: `Not a menu choice '<pick>'. Type 1, 5, 6, 7, or 9, or a listed name.`

Choosing **5** or typing `sudoers` **on this board** **MUST** open the sudoers board (`requirement-shell-cli-sudoers-submenu`). A sudoers **leaf** returns to **this** front board. Sudoers **Back** reprints **this** front board.

#### 2.3.2 Client board (front **1**)

Header title: `client-side`.

| # | Token | Label |
|---|-------|-------|
| 11 | `backup` | `backup: Pack a named folder into a dated gzip archive under /var/backup/folder-backup` |
| 12 | `restore` | `restore: Put an archive back onto the hard-disk projects tree` |
| **0** | **Back** | return to the front board |

A backup or restore leaf returns to the **front**. Invalid client text: `Not a menu choice '<pick>'. Type 11, 12, or 0, or a listed command name.` Number **17** is not a row on this board.

#### 2.3.3 Self board (front **6**, and verb `self-management`)

Header title: `self-management`. This product is **dual** place: local copy and channel place are both shown. Labels are the kept-list human-readable explains.

| # | Token | Label |
|---|-------|-------|
| 61 | `install` | `install: Copy this program into your bin or /usr/local/bin` |
| 62 | `version` | `version: Show version and detailed diagnostics (about)` |
| 63 | `about` | `about: Show diagnostics including sudoers trust tier` |
| 64 | `version-check` | `version-check: Compare this version with the channel` |
| 65 | `self-update` | `self-update: Replace the placed binary from the channel` |
| 66 | `self-uninstall` | `self-uninstall: Remove the channel-placed binary` |
| 67 | `self-install` | `self-install: Copy this file, or download it when the shell is a pipe` |
| **0** | **Back** | return to the caller |

`uninstall` and `where-is-me` stay **typed commands**. Their absence is **not** a hide cause (no hide sentence on this board). **61** is the local copy. **67** is the channel place. **66** is channel remove, not local `uninstall`. On this board, row **62** and a typed `version` **MUST** run `app_about`. Argv `folder-backup version` stays `app_version` (the thin version line). Row **63** also runs `app_about`.

Opened from the front, Back **and** a finished leaf both return to the front. Opened as the argv verb `self-management`, the self board is the whole session: a leaf runs and the verb ends; Back ends the verb; the front board is not opened. Handler: `app_cmd_menu_self`. `app_default_self_loop` saves JSON and QUIET, and on a terminal calls `app_cmd_menu_self`. Off a terminal it stops with `self-management needs a terminal`. Invalid self text: `Not a menu choice '<pick>'. Type 61-67, 0 back, or a listed command name.`

### 2.4 Sudoers board (owned elsewhere)

Front row **5** / `sudoers` **MUST** open the grant/draft board. Membership, reserved numbers **51** / **53** / **54**, Back **0**, the hide sentence, and the live-verb rule **MUST** follow **`requirement-shell-cli-sudoers-submenu`**. This file **MUST NOT** restate that table as a second SSOT.

### 2.5 Implementation Notes (this product)

| Item | Value |
|------|--------|
| **Product** | `folder-backup` |
| **Claimed** | yes |
| **Case** | **2** for the interactive zero-cli-verb. Non-interactive place is `requirement-shell-cli-zero-arguments` |
| **Empty argv owner** | **Split.** This file: interactive boards. Zero-arguments: non-interactive `inst_self_install` |
| **Menu verbs** | empty argv on TTY; `menu` (preferred named); `main` alias |
| **Handlers** | `app_cmd_menu` · `app_cmd_menu_client` · `app_cmd_menu_language` · `app_cmd_menu_self` · `app_cmd_menu_sudoers` · `app_lang_load` · `app_lang_save` · `app_menu_text` |
| **Aliases** | `app_main_menu` → `app_cmd_menu`; `app_default_self_loop` → `app_cmd_menu_self` |
| **Family row** | front **5** `sudoers` — menu-only; **not** dispatched; body **`requirement-shell-cli-sudoers-submenu`** |
| **Ship unit** | Implemented — `app_main` empty argv and `menu` / `main` call `app_cmd_menu` |
| **Kept list** | `reviews/cli-routed-verb-table.md` |
| **Look** | Default CLI main menu style — header `folder-backup(VERSION)`; TTY bold short name; TTY italic + light-gray explain; `out_menu_choice` / `util_app_ident` |
| **Choice read** | Numbered boards: `out_msg_n` of the choose-prompt, then current-shell `read -r` → `_prompt_line` (not `$()`). Field prompts stay `prompt_line` |
| **Front** | **1** / **5** / **6** / **7** / **9**; number **2** reserved and hidden |
| **Language** | Front **7**; body **`requirement-shell-cli-language`** |
| **Exit** | **9** on the front only |
| **Back** | **0** on child boards |
| **Test-purpose (this product)** | `print-sudoers`, `print-sudoers-install-script`, `generate-sudoer-request` — off **every** numbered board |
| **Typed-only (not a hide cause)** | `uninstall`, `where-is-me` |
| **Zero-cli-verb peer** | `requirement-shell-cli-zero-arguments` (Active) |
| **Honesty** | **Implemented** (suite **TP-CLI-13** · **TP-CLI-14** · **TP-CLI-16** · **TP-CLI-18** · **TP-CLI-19** · **TP-CLI-21** · **TP-CLI-24**) |

**Normative front draft** (README / this fence use markdown emphasis; the live TTY uses SGR, never paste CSI here):

```text
[INFO] **folder-backup**(*VERSION*) — numbered list
[INFO] server-side is not available: this program does not run a host service. Number 2 stays reserved.
1. **client-side**: *this login's folders: pack and restore*
5. **sudoers**: *Grant and drafts*
6. **self-management**: *this CLI install, version, update, uninstall*
7. **language**: *display language for this menu*
9. Exit
```

**Invocation samples (CI-M1a):**

```text
folder-backup
folder-backup menu
folder-backup main
folder-backup menu --json
folder-backup self-management
folder-backup generate-sudoer-request
folder-backup submit-sudoer-request
folder-backup print-sudoers
folder-backup print-sudoers-install-script
folder-backup remove-project-sudoers
```

On a real terminal the first three **MUST** show the front board. `folder-backup menu --json` on a real terminal **MUST** still show the front board. `folder-backup self-management` on a real terminal **MUST** show the self board and **MUST NOT** show the front board first. Off a terminal, `folder-backup` with no command **MUST** place the program. Off a terminal, `folder-backup menu` and `folder-backup self-management` **MUST** stop (`menu needs a terminal` / `self-management needs a terminal`, exit 1). `folder-backup --json` with no command **MUST** place the program. `folder-backup menu --json` off a terminal **MUST** be a JSON error, not JSON help. An empty line on the front **MUST** leave. Row **62** and a typed `version` on a board **MUST** run `about`. The five grant/draft names **MUST** run as live commands. `folder-backup sudoers` **MUST** fail as unknown.

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Empty argv has one owner (this file, case 2). Daily folder work is client-side. This program’s own place and update is self-management. There is no host service, so server-side stays reserved.  
- **Principle 1 – Caution**: Scripts do not hang. A pipe with no command places the CLI. An interactive line does not.  
- **Principle 16 – Interactive vs non-interactive**: TTY vs pipe is explicit.  
- **Principle 10 – Least privilege**: `sudoers` is not a dispatcher token. Test-purpose grant-emit stays off every numbered board.

---

## Under command line for normal user only

When this program runs on Termux, Git Bash, Windows Command Prompt, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** the numbered boards may still show backup/restore; picking them **MUST** fail closed on that class rather than wrapping `sudo`.

| MUST | MUST NOT |
|------|----------|
| Numbered boards as this login | Hang; wrap sudo to place this program |
| Git Bash / Windows cmd: no Termux `pkg` | Treat WSL as this class |

Detect (typical): Termux — `PREFIX` contains `com.termux` or `TERMUX_VERSION` is set. Git Bash — `MSYSTEM` is `MINGW*` / `MSYS*`. Windows cmd — `OS=Windows_NT` and `COMSPEC` names `cmd.exe` after excluding Git Bash, Cygwin, and WSL.

**Implementation Notes:** ship unit has **no detect helper yet** (Gap).

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not hang off-TTY. Do not place on an interactive zero-cli-verb. Do not print help for a non-interactive zero-cli-verb.  
- **Intentional:** Case 2; labels from the kept list; domain categories use parent-prefix numbers.  
- **Anti-fragile:** `menu` / `main` open the same boards as a bare TTY run; Back **0** returns to the parent; a finished leaf redisplays the front.  
- **Over-protect:** Test-purpose verbs stay off every numbered board; front Exit is **9**; child Back is **0**; number **2** stays reserved.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Route a non-interactive zero-cli-verb to help, or withdraw `requirement-shell-cli-zero-arguments`.  
2. Place the program on an interactive zero-cli-verb, or call `inst_local_install` from that line.  
3. Invent menu labels instead of `command: what it does` from the kept list (category rows use this file’s table).  
4. Put `help`, `menu`, `main`, `uninstall`, `where-is-me`, or a test-purpose verb (`print-sudoers`, `print-sudoers-install-script`, `generate-sudoer-request`) on any numbered board.  
4b. Put `backup`, `restore`, or the five grant/draft verbs on the **front** board.  
4c. Restate sudoers-board membership as a second SSOT here (that table lives on **`requirement-shell-cli-sudoers-submenu`**).  
4d. Print a server-side row, or add `app_cmd_menu_server`, while this program has no host service.  
5. Restart a child board at **1**, compact a hidden number, number front Exit as anything other than **9**, or print Back as a front-row number / Exit **9** on a child board. Child Back **MUST** be **0**.  
6. Draw the menu on a non-interactive zero-cli-verb, or on off-TTY `menu` / `self-management`. Off-TTY named menu **MUST** stop; it **MUST NOT** print help.  
7. Treat interactive `folder-backup menu --json` as JSON help.  
7b. Send row **62** or a typed `version` on a numbered board to the thin `app_version` line. Argv `version` stays that thin line.  
7c. Treat an empty line on the front as an invalid choice. Empty on the front is Exit.  
8. Drop `menu`/`main` routing after attaching the boards to empty argv.  
9. Auto-write `/etc` from a menu choice (print/submit stay Type 0 drafts).  
10. Claim the ship unit lacks the TTY empty-argv menu while `app_main` routes empty argv to `app_cmd_menu`.  
11. Capture the menu choice (or extra field) with `$()` / backticks of a `read` helper, or “fix” a freeze by stderr+$() (**PP-A-22** / do-not-capture-read).  
12. Print a board header as a bare `folder-backup` without live `VERSION`, or unstyled on a TTY.  
13. Draw a numbered board off the default CLI main menu style — short name **MUST** be bold on a TTY; `explain` **MUST** be *italic* and light gray. **MUST NOT** emit CSI off-TTY.  
14. Wire `sudoers` as a live `app_main` command.  
15. Exit the menu after a successful leaf, or stay on the child board that launched it, when the operator entered from the front.  
16. Treat `uninstall` / `where-is-me` absence from the self board as a hide cause.

**Violating this rule is a critical dispatcher / hang / honesty / look regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | A non-interactive zero-cli-verb does not draw these boards (place is `requirement-shell-cli-zero-arguments`) |
| AC-2 | Case 2 recorded for the interactive line; `menu` / `main` named and routed to `app_cmd_menu` |
| AC-3 | Interactive empty argv **and** interactive `menu` draw the front board: hide sentence, **1** client-side, **7** language, **5** sudoers, **6** self-management, **9** Exit; row **2** is not printed |
| AC-4 | Interactive `menu --json` still draws the front board |
| AC-5 | Non-interactive `menu` / `main` / `self-management` exit 1 with `needs a terminal` (JSON error when `--json`). `--json` **with no command** is self-install, not JSON help |
| AC-6 | No numbered board lists `help`, `menu`, `main`, `uninstall`, `where-is-me`, or a test-purpose verb. The front board does not list backup, restore, or the five grant/draft verbs |
| AC-7 | Leaf labels match kept-list human-readable `verb: explain`; category explains are this file’s tables |
| AC-8 | TTY header is live `folder-backup(VERSION)` with bold name and italic version; short name is bold; numbered `explain` is italic and light gray; number, Exit, and Back stay unstyled; no CSI off-TTY |
| AC-9 | Menu choice is current-shell `read -r` into `_prompt_line` after the language choose-prompt; **MUST NOT** `$()` a `read` helper |
| AC-10 | Client **1** lists **11** / **12** / **0** Back. Front **5** opens the sudoers board (**`requirement-shell-cli-sudoers-submenu`**). Self **6** lists **61**–**67** and **0** Back |
| AC-11 | `folder-backup sudoers` is unknown. Typing `sudoers` or **5** on the front opens the sudoers board. Typing `sudoers` on the client is invalid. The five grant/draft names remain live CLI verbs |
| AC-12 | A finished leaf redisplays the front board. An invalid child number reprints the front board. Typing **2** is an invalid retry. An empty line on the front leaves |
| AC-13 | Row **62** and a typed `version` on a board run `about`. Argv `folder-backup version` stays the thin version line |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-shell-cli-zero-arguments` | **Active** owner of the non-interactive zero-cli-verb (`inst_self_install`) |
| `requirement-shell-cli-interface` | Dual mention: empty argv row + `menu` / `main` + self board on the command table |
| `requirement-shell-cli-sudoers-submenu` | Front row **5** / `sudoers`; sudoers-board membership and live-verb rule |
| `requirement-shell-cli-language` | Front row **7**; eight codes; menu copy follows `APP_LANG` |
| `requirement-shell-interactive-vs-noninteractive` | `TTY`; no hang |
| `requirement-shell-output-requirements` | `out_*`; bold short name; reuse `app_help` |
| `requirement-shell-local-self-management` | `install` is self row **61**; `uninstall` / `where-is-me` stay typed |
| `requirement-domain-folder-backup` | Grant-emit verbs; help apart; off every numbered board |
| `docs/requirements/index.md` | Registry |

---

## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-07** | `tests/test_cli.sh` | **have** — off-TTY empty argv places the CLI, not these boards (AC-1) |
| **TP-CLI-13** | `tests/test_cli.sh` | **have** — front board, client **11**/**12**, sudoers **52**/**55**, hide sentences, `sudoers` not dispatched (AC-3 / AC-10 / AC-11) |
| **TP-CLI-14** | same | **have** — interactive `menu --json` still prints the front board (AC-4) |
| **TP-CLI-15** | same | **have** — non-interactive `menu` and `self-management` stop (`needs a terminal`, exit 1) (AC-5) |
| **TP-CLI-23** | same | **have** — `--json` / `--quiet` with no verb place; TTY `--debug` draws the front (AC-5 / AC-3) |
| **TP-CLI-16** | same | **have** — front shows **6** self-management and omits verb rows that belong on a child board (AC-6) |
| **TP-CLI-18** | same | **have** — bold short name, italic light-gray explain, unstyled Exit, sudoers title (AC-8) |
| **TP-CLI-19** | same | **have** — child number **12** on the front is invalid and the front reprints (AC-12) |
| **TP-CLI-21** | same | **have** — empty Enter leaves the front; row **62** and typed `version` run `about`; the front reprints (AC-12 / AC-13) |
| **TP-CLI-24** | same | **have** — front **7** stores one of eight codes (`requirement-shell-cli-language`) |

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
| 2026-10-14 | Active 1.13.0 | Front **5** sudoers, **6** self-management, **7** languages. Children keep the parent prefix: sudoers **52**/**55** (reserved **51**/**53**/**54**), self **61**–**67**, language **71**–**78**. The front sample prints **1**, **5**, **6**, **7**, **9**. | Terminologies section added.
| 2026-08-23 | Active 1.0.0 | Case 3 claimed; menu/main Gap; nine-row list; Exit 99 |
| 2026-08-23 | Active 1.1.0 | Colon labels; exclude version/about; test-purpose print-sudoers / generate-sudoer-request / print-sudoers-install-script; N=4 Exit 9 |
| 2026-08-23 | Active 1.2.0 | Ship unit routes `menu` / `main`; Gap closed; empty argv stayed help (case 3) |
| 2026-08-28 | Active 1.3.0 | **Case 2**: TTY empty argv = numbered list; off-TTY empty argv = help; zero-arguments Withdrawn |
| 2026-09-03 | Active 1.4.0 | Default CLI main menu style (header nametag + TTY gray italic explain); do-not-capture-read MUST; **TP-CLI-18** |
| 2026-09-03 | Active 1.5.0 | Family row **sudoers** + submenu (five grant/draft setup verbs remain live CLI commands; Back 8 / Exit 9); main **N = 3**; `sudoers` not dispatched |
| 2026-09-03 | Active 1.6.0 | Submenu **body** moved to **`requirement-shell-cli-sudoers-submenu`**; this file keeps the family row on the start list |
| 2026-09-30 | Active 1.6.1 | Channel verbs are live and stay off the flat list. Case 2 still owns empty argv. |
| 2026-09-30 | Active 1.7.0 | Hierarchical boards: front **1** / hidden **2** / **8** / **9**; client **11**/**12**/**17**; self **81**–**87**; child Back **0**; finished leaf redisplays the front; short name bold |
| 2026-09-30 | Active 1.8.0 | Non-interactive zero-cli-verb moves to `requirement-shell-cli-zero-arguments` (self-install). This file keeps the interactive boards. Named `menu` off-TTY stays help. |
| 2026-09-30 | Active 1.9.0 | Named `menu` / `main` / `self-management` off a terminal stop (`needs a terminal`). Empty Enter on the front leaves. Row **82** and a typed `version` on a board run `about`. Argv `version` stays the thin line. Interactive `menu --json` still draws. |
| 2026-09-30 | Active 1.10.0 | Sudoers moves from client **17** to front **7**. Client is **11** / **12**. Sudoers children are **72** and **75**. Reserved **71** / **73** / **74**. Back from sudoers returns to the front. |
| 2026-09-30 | Active 1.11.0 | Front **6** language. English catalog stays this file. Other languages and the language file are `requirement-shell-cli-language`. Menu boards read the choose-prompt in the current shell. |
| 2026-10-10 | Active 1.13.0 | Front hide sentence says server-side is not available. Number **2** stays reserved. |

---

**Last Updated**: 2026-10-14  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
