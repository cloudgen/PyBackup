**file**: docs/requirements/requirement-shell-cli-sudoers-submenu.md  
**Status**: Active (Version 1.5.0)  
**Area**: shell  
**Key**: `requirement-shell-cli-sudoers-submenu`  
**Optional RQ-ID**: `RQ-SHELL-CLI-SUDOERS-SUBMENU`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **product Single Source of Truth** for folder-backup’s **sudoers board**: opened from front row **5**, listing only the operational grant/draft verbs, and keeping the test-purpose numbers reserved. The front, client, and self boards stay on `requirement-shell-cli-default-interaction`. JSON grant **body** stays on `requirement-sudoer-json-file`. Emit / submit **workflow** stays on `requirement-three-layer-privilege-model`.

This file exists so the sudoers board is a **named, transferable** product law — not a buried paragraph on the front-board requirement.

### 1.1 Human-facing

**In one sentence:** On a real terminal, pick front **5** to hand in a grant or remove a local draft; the three test commands stay typed, not numbered; typing `sudoers` as a command is unknown.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Open the grant board or type an operational verb | `folder-backup` then `5` |
| The other role | Scripts type the five names; they never hang on this board | `folder-backup generate-sudoer-request` |
| Not this file | Front, client, and self rows; empty argv; JSON grant body | `requirement-shell-cli-default-interaction` · `requirement-sudoer-json-file` |

| Includes | Excludes |
|----------|----------|
| Front family row **5** `sudoers` (menu-only) | `sudoers` as a typed command |
| Operational rows **52** and **55** | Test-purpose rows on this board |
| Reserved numbers **51**, **53**, **54** | Those numbers reused or compacted |
| **0** Back | Back as a front-row number or Exit **9** on this board |
| One hide sentence for the test commands | Install / version / about on this board |

| Surface | What you open | What for |
|---------|---------------|----------|
| `./src/folder-backup` | ship unit | live menu + live setup verbs |
| `folder-backup help` | command | listed setup verbs, test-purpose under their own heading |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open grant/drafts | Operational rows only | `folder-backup` then `5` |
| Queue inbound | Same handler as row **52** | `folder-backup submit-sudoer-request` |
| Remove local draft | Same handler as row **55** | `folder-backup remove-project-sudoers` |
| Write a JSON grant | Typed command. Not a numbered row. | `folder-backup generate-sudoer-request` |
| Emit sudoers text | Typed command. Not a numbered row. | `folder-backup print-sudoers` |
| Write admin script | Typed command. Not a numbered row. | `folder-backup print-sudoers-install-script` |
| Step back to the front | Back | `0` |
| Type the family name as a command | Unknown — not a command | `folder-backup sudoers` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Claim

1. This product **claims** a sudoers board under the front board.  
2. A claimed front board is required (`requirement-shell-cli-default-interaction`).  
3. **MUST NOT** hang off-TTY (this board exists only on the interactive menu path).

### 2.2 Family row

1. The family token **MUST** be `sudoers`. Explain **MUST** be `Grant and drafts`. The number **MUST** be front **5** (owned as a row by `requirement-shell-cli-default-interaction`).  
2. **`sudoers` is not a live CLI command.** Choosing **5** or typing `sudoers` at the **front** pick prompt **MUST** open this board. Typing `sudoers` at the **client** pick prompt **MUST** be an invalid choice on the client. `folder-backup sudoers` **MUST** remain unknown.  
3. **MUST NOT** list the five setup verbs on the **front** board or the **client** board.

### 2.3 Sudoers board — operational grant and drafts

Choosing front **5** / `sudoers` **MUST** print this board. Header **MUST** use the same `folder-backup(VERSION)` nametag. Title when `APP_LANG=en`: `sudoers (grant and drafts)`. Other codes translate the header and the longs and keep the English verb shorts (`requirement-shell-cli-language`). Explain text **MUST** follow the same default CLI main menu style as the other boards (short name bold; explain italic and light gray). The hide sentence and the invalid text below are the English sentences.

Print this hide sentence **before** the numbers (exact):

`test commands are not available: type generate-sudoer-request, print-sudoers, or print-sudoers-install-script. Numbers 51, 53, and 54 stay reserved.`

| # | Command | Label | Setup kind |
|---|---------|-------|------------|
| **51** | `generate-sudoer-request` | **reserved — not printed** | JSON grant (test-purpose) |
| 52 | `submit-sudoer-request` | `submit-sudoer-request: Hand the JSON grant to the approval queue` | Inbound queue |
| **53** | `print-sudoers` | **reserved — not printed** | sudoers text (test-purpose) |
| **54** | `print-sudoers-install-script` | **reserved — not printed** | Admin script (test-purpose) |
| 55 | `remove-project-sudoers` | `remove-project-sudoers: Remove the local grant draft only` | Remove draft |
| **0** | **Back** | return to the front board (not a command) | — |

- **0** / `back` / `Back` / empty line / EOF / `exit` / `quit` returns to the **front** board (does not run a handler, does not leave the whole menu).  
- A listed number or listed verb runs that handler, then returns to the **front** board (command finished).  
- **51**, **53**, and **54** **MUST** stay reserved. **MUST NOT** print those rows. **MUST NOT** compact **52** and **55** down to 1 and 2.  
- All five grouped verbs **MUST** remain live CLI verbs. Only **52** and **55** appear on this board.  
- **MUST NOT** put `install` / `version` / `about` / `help` / `menu` / `main` on this list.  
- Typing `submit-sudoer-request` or `remove-project-sudoers` at the **front** pick prompt **MUST** run that handler, then redisplay the front. Typing a test-purpose name at a menu prompt **MUST** be an invalid choice; those names run as argv commands.  
- Choice **MUST** be read in the **current shell**. **MUST NOT** `$()` a `read` helper.  
- Invalid text: `Not a menu choice '<pick>'. Type 52, 55, or 0, or a listed command name.`

### 2.4 Implementation Notes (this product)

| Item | Value |
|------|--------|
| **Product** | `folder-backup` |
| **Claimed** | yes |
| **Family token** | `sudoers` |
| **Family number** | front **5** |
| **Handler** | `app_cmd_menu_sudoers` |
| **Printed members** | `submit-sudoer-request` (**52**) · `remove-project-sudoers` (**55**) |
| **Reserved, not printed** | `generate-sudoer-request` (**51**) · `print-sudoers` (**53**) · `print-sudoers-install-script` (**54**) |
| **Choice read** | Current-shell `prompt_line` → `_prompt_line` |
| **Return** | leaf returns so the front redisplays; Back returns so the front board reprints |
| **Honesty** | **Implemented** |

**Invocation samples:**

```text
folder-backup generate-sudoer-request
folder-backup submit-sudoer-request
folder-backup print-sudoers
folder-backup print-sudoers-install-script
folder-backup remove-project-sudoers
```

### 2.5 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: The grant board is a named law. Operators see the two verbs they run. Test commands stay typed.  
- **Principle 1 – Caution**: `sudoers` is never dispatched; scripts do not hang.  
- **Principle 21 – Dual policies**: Portable catalog of setup kinds; this product prints only the operational rows and reserves the rest.  
- **Principle 10 – Least privilege**: Print/submit stay Type 0 drafts; the menu never writes `/etc`.

---

## Under command line for normal user only

When this program runs on Termux, Git Bash, Windows Command Prompt, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** grant/draft setup verbs stay Type 0 drafts; this board **MUST NOT** install `/etc`.

| MUST | MUST NOT |
|------|----------|
| Print / generate JSON as this login | Wrap `sudo` from a menu pick |
| Git Bash / Windows cmd: no Termux `pkg` | Treat WSL as this class |

Detect (typical): Termux — `PREFIX` contains `com.termux` or `TERMUX_VERSION` is set. Git Bash — `MSYSTEM` is `MINGW*` / `MSYS*`. Windows cmd — `OS=Windows_NT` and `COMSPEC` names `cmd.exe` after excluding Git Bash, Cygwin, and WSL.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Family token unknown; no hang off-TTY.  
- **Intentional:** Operational rows are explicit. Test-purpose numbers stay reserved.  
- **Anti-fragile:** Typed member verbs still run without the menu.  
- **Over-protect:** Test-purpose verbs stay off every numbered board; Back is **0**.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Wire `sudoers` as a live `app_main` command.  
2. Drop `submit-sudoer-request` or `remove-project-sudoers` from this board while they remain live.  
3. Put the five setup verbs on the **front** board, or put a test-purpose verb on this board.  
4. Number Back as anything other than **0**, print Exit **9** on this board, or reuse **51** / **53** / **54**.  
5. Hang off-TTY on this board’s path.  
6. Capture the choice with `$()` of a `read` helper.  
7. Auto-write `/etc` from a menu choice.  
8. Collapse this file back into `requirement-shell-cli-default-interaction` as the only owner.  
9. Compact **52** and **55** because the reserved rows are hidden.

**Violating this rule is a critical dispatcher / hang / transferability regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Front family row is **5** `sudoers: Grant and drafts` |
| AC-2 | Choosing **5** / `sudoers` at the front prompt opens this board with **52**, **55**, the test-command hide sentence, and **0** Back. Rows **51**, **53**, and **54** are not printed |
| AC-3 | `folder-backup sudoers` is unknown |
| AC-4 | The five names remain live CLI verbs |
| AC-5 | The five names are **not** front-board rows. The three test-purpose names are **not** on this board |
| AC-6 | Board nametag is live `folder-backup(VERSION)`; title is `sudoers (grant and drafts)` |
| AC-7 | Choice is current-shell `prompt_line` / `_prompt_line` |
| AC-8 | A finished **52** or **55** returns to the front board. **0** returns to the front board |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-shell-cli-default-interaction` | Front and client boards; **points** here for row **5** |
| `requirement-shell-cli-interface` | Dual mention: five setup verbs remain routed |
| `requirement-domain-folder-backup` | Domain catalog of those verbs; help apart; test-purpose off numbered boards |
| `requirement-sudoer-json-file` | JSON grant **body** |
| `requirement-three-layer-privilege-model` | Emit / submit **workflow** |
| `requirement-shell-interactive-vs-noninteractive` | `TTY`; no hang |
| `requirement-shell-output-requirements` | `out_menu_choice` |
| `docs/requirements/index.md` | Registry |

---

## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-13** | `tests/test_cli.sh` | **have** — front **5**, rows **52**/**55**, hide sentence, no **51** row, Back **0**, `sudoers` unknown, members live (AC-1–AC-5) |
| **TP-CLI-16** | same | **have** — grant verbs off the **front** board (AC-5) |
| **TP-CLI-18** | same | **have** — sudoers title and bold short name (AC-6) |

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
| 2026-10-14 | Active 1.5.0 | Opened from front row **5**. Printed rows **52** and **55**. Reserved **51**, **53**, and **54**. | Terminologies section added.
| 2026-09-03 | Active 1.0.0 | Dedicated sudoers-submenu SSOT; five setup kinds on the second board; Back 8 / Exit 9 |
| 2026-09-30 | Active 1.1.0 | Opened as client **17**. Printed rows **172** and **175** only. **171**/**173**/**174** reserved. Back **0**. A leaf returns to the front |
| 2026-09-30 | Active 1.2.0 | Opened as front **7**. Printed rows **72** and **75**. **71**/**73**/**74** reserved. Back **0** returns to the front |
| 2026-09-30 | Active 1.2.1 | Header, longs, hide sentence, and invalid text follow `APP_LANG`. English strings stay this table. Numbers stay **72** / **75**. |
| 2026-10-10 | Active 1.4.0 | Hide sentence matches the front board: test commands are not available, then the typed names, then numbers **71** / **73** / **74** stay reserved. |

---

**Last Updated**: 2026-10-14  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
