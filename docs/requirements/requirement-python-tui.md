**file**: docs/requirements/requirement-python-tui.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-tui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the picture of PyBackup’s text menu. The screen has a menu region and a bottom input box. The first menu row keeps the current path on the left and, when that row has room, a local clock `HH:MM:SS` on the right. The status line shows the product name and the version. A three-row light band under the input box says which feature is not available. That band is the features-non-available message box. The status line stays the last row.

The session is class `Tui` in `src/PyBackup/tui.py`. The frame is class `MenuPainter` in `src/PyBackup/menu_painter.py`. `def main` stays in `src/PyBackup/cli.py`. The product does not import another menu package.

HelloTui rows **3**, **4**, **8**, and **9** stay. Folder-backup replaces HelloTui row **1** (`hello`) with **client-side** and adds front row **5** sudoers. Row **2** stays unprinted.

There is no Python text-menu mold. This file is the product picture.

Project nature: a command-line program whose empty line on a terminal is a numbered menu.

### 1.1 Human-facing

**In one sentence:** On a terminal, `py-backup` with no arguments shows a numbered menu, a rounded box, three light lines under that box, and a status line.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You see the front board and type a number | `py-backup` |
| The other role | Backup and restore are on the client board, not the front board | Rows 11 and 12 |
| Not this file | The words of each language, and the packing steps | Language and backup requirements |

| Includes | Excludes |
|----------|----------|
| Path and clock, numbered rows, three-row box, three-row light band, status line | A `Choice:` line, `print` / `read`, or `input()` for that menu |
| Rows 1, 3, 4, 5, 8, 9 | A printed row 2, and renumbering 3, 4, 8, or 9 |

| Surface | What you open | What for |
|---------|---------------|----------|
| `py-backup` | the menu | the front board |
| `README.md` | the text fence | the same rows, described as the current directory |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the menu | No extra words on a terminal draws the front board. Off a terminal the same empty line prints help and does not draw. | `py-backup` |
| Leave | Row 9 returns 0. There is no confirm. | Choose 9 |

## 2. Core Rules (Mandatory)

1. The text-menu session **MUST** be class `Tui`. The frame **MUST** be class `MenuPainter`. `cli.py` **MUST NOT** contain the frame glyphs. The menu **MUST NOT** use `input()`.
2. Front rows **MUST** be **1** client-side, **3** system-log, **4** language, **5** sudoers, **8** self-management, **9** Exit. Row **2** is omitted. **MUST NOT** renumber 3, 4, 8, or 9. **MUST NOT** list `hello`. **MUST NOT** list backup, restore, or a grant verb on the front board.
3. Client-side **MUST** list **11** backup, **12** restore, and **0** Back.
4. System-log **MUST** list **31** view-log, **32** clear-log, **33** log-folder, and **0** Back.
5. Language **MUST** list **41** through **53** and **0** Back. Codes stay on `requirement-python-cli-language`. `language` is not an argv verb.
6. Sudoers **MUST** list **52** submit-sudoer-request, **55** remove-project-sudoers, and **0** Back. Numbers **51**, **53**, and **54** stay unprinted. Test-purpose verbs stay off every numbered board.
7. Self-management **MUST** list **82** version, **83** about, **84** version-check, **85** self-update, **86** self-uninstall, **87** self-install, and **0** Back. Pip commands **MUST** be `python -m pip` and **MUST NOT** use `sudo` or `curl`. No row **81**.
8. The bottom box **MUST** be three rows: `╭` `─` `╮`, `│` with `> ` and caret `█` when focused, `╰` `─` `╯`. ASCII `+` `-` `|` **MUST NOT** stand in. The status line **MUST** be the last row and **MUST** show name, version, board title, and `Up/Down  •  Enter`.
9. Under the box and above the status line, the front board and the sudoers board **MUST** draw exactly three light rows. English sentences stay exact. Other codes use `requirement-python-cli-language`. A result page **MUST NOT** draw the sentence. The band does not take keys.
10. English front sentence: `server-side is not available: this program does not run a host service. Number 2 stays reserved.`
11. English sudoers sentence: `test commands are not available: type generate-sudoer-request, print-sudoers, or print-sudoers-install-script. Numbers 51, 53, and 54 stay reserved.`
12. Column widths are display columns. East Asian Wide and Fullwidth count as two. Ambiguous stays one.
13. The path line **MUST** be `<label>: <absolute cwd>`. English label is `Path`. Traditional Chinese is `路徑`. The path and the clock are not translated. The clock is local `HH:MM:SS`. Boards that show the clock (front, client, sudoers, system-log, language, self-management) wait at most one second and **MUST NOT** start a thread. A no-key is not Esc and is not Exit.
14. A screen that cannot hold the path line, one menu row, the box, the three-row band, and the status line **MUST** fail closed. Empty argv off a terminal **MUST NOT** draw this screen.
15. Exit **9** returns 0 with no confirm. An unknown token stays on the board.

### 2.1 Screen parts

| Part | What it is | Where it sits | Display style |
|------|------------|---------------|---------------|
| Navigation | Numbered rows | Menu region | Number, short name, explain |
| Status | Name, version, board title, keys | Last row | Plain status line |
| Major input | The bottom box | Under the menu | Three-row rounded box, caret `█` |
| Major output | The menu rows and result pages | Above the box | The painter, not `print` |
| Path display | Current directory | First menu row, left | Label plus absolute path |
| System-time display | Local clock | First menu row, right, when it fits | `HH:MM:SS` |
| Time-consuming process messages | Not used | This program does not download a model or convert images | No waiting sentence |

This release does not add a screenshot file. The README text fence is the capture already described in `requirement-python-readme`. This file does not invent a second picture.

### 2.2 Implementation Notes

| Field | Value |
|-------|--------|
| Command | `py-backup` |
| Package | `src/PyBackup` |
| Front explains (English) | client-side: this login's folders: pack and restore; sudoers: Grant and drafts |
| Backup explain | Pack a named folder into a dated gzip archive under /var/backup/PyBackup |
| Bootstrap | HelloTui architecture. HelloTui is not edited |

### 2.3 Code example

```python
FRONT_ROWS = (1, 3, 4, 5, 8, 9)

FRONT_BAND_EN = (
    "server-side is not available: this program does not run a host service. "
    "Number 2 stays reserved."
)
```

```text
py-backup
```

The major entry is that empty command on a terminal. `py-backup backup /path/to/project` stays on the terminal unless the missing-operand rule asks in the box.

## 3. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Front numbers are 1, 3, 4, 5, 8, 9 |
| AC-2 | System-log 31–33, language 41–53, self-management 82–87 |
| AC-3 | Sudoers prints only 52, 55, and Back |
| AC-4 | English band sentences match rules 10 and 11 |
| AC-5 | `hello` is not a row and not a verb |

## Terminologies

### Major TUI entry point

**Definition:** Major TUI entry point is the rule that the major entry of a claimed text screen is interactive mode with no positional command token. Flags that are not a command stay on that entry. `--json` with no command stays JSON help, not the text screen. Creating or keeping a text screen does not attach every CLI verb to that screen. A verb opens the screen only when a specialized requirement explicitly names that verb as using the text screen.

**Human daily-life explanation:** A major TUI entry point is the walk-up board at a shop. You see that board when you name no dish. Naming a dish sends you to a different counter.

**Daily-life example:** You type `py-backup` and see the front board. You type `py-backup backup /path/to/project` and that job stays at the plain counter, except when the folder is missing and a terminal asks in the box.

## 4. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | Text menu picture for `py-backup` |
| 2026-10-22 | Active 1.0.1 | Voice pack, screen-part table, front-row sample. No new screenshot. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
