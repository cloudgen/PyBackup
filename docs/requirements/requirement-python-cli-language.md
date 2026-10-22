**file**: docs/requirements/requirement-python-cli-language.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-cli-language`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

This file owns the menu language: thirteen codes, the leaf, and which sentences move with the code. The board that lists them is `requirement-python-tui`.

Project nature: a command-line program whose menu can change language. `language` is not a command you type.

### 1.1 Human-facing

**In one sentence:** The menu language is a one-word file under `~/.local/PyBackup/language`, and `PYBACKUP_LANG` wins for one run without writing that file.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You pick a code on the language board. The leaf is mode 0600. | Code 41 is English |
| The other role | The shell file uses a different variable name | That file is not `py-backup` |
| Not this file | Which rows are printed | The text-menu requirement |

| Includes | Excludes |
|----------|----------|
| Codes 41–53, the leaf, `PYBACKUP_LANG` | An argv verb named `language` |
| English band sentences left exact | Invented translations for `ar`, `pt`, `ru`, `nl`, and `el` domain lines |

| Surface | What you open | What for |
|---------|---------------|----------|
| `~/.local/PyBackup/language` | one code | the saved language |
| `PYBACKUP_LANG` | one process | override, no write |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Force English for one run | The leaf stays as it was. This process uses English. | `PYBACKUP_LANG=en py-backup help` |

## 2. Core Rules (Mandatory)

1. Codes **MUST** be 41 English, 42 简体中文 (`zh-Hans`), 43 繁體中文 (`zh-Hant`), 44 Español (`es`), 45 العربية (`ar`), 46 Français (`fr`), 47 Português (`pt`), 48 Русский (`ru`), 49 Deutsch (`de`), 50 日本語 (`ja`), 51 한국어 (`ko`), 52 Nederlands (`nl`), 53 Ελληνικά (`el`).
2. The leaf **MUST** be `~/.local/PyBackup/language`, one code, mode 0600. The directory mode is 0700. `LANG` **MUST NOT** select the menu language.
3. `PYBACKUP_LANG`, when it is one of the thirteen codes, **MUST** win for that process and **MUST NOT** write the leaf.
4. HelloTui translations for system-log, language, self-management, Exit, Back, and the pip rows **MUST** stay. The welcome sentence **MUST NOT** stay. Client-side, sudoers, backup, restore, submit, remove, and the two not-available sentences **MUST** use the folder-backup catalog for `en`, `zh-Hans`, `zh-Hant`, `es`, `fr`, `de`, `ja`, and `ko`. `ar`, `pt`, `ru`, `nl`, and `el` **MAY** fall back to English for those domain sentences.
5. English front and sudoers band sentences **MUST** stay the exact sentences in `requirement-python-tui`. The backup sentence names `/var/backup/PyBackup`.
6. English help headings **MUST** stay exact. The other seven folder-backup codes translate the two headings.
7. The path value and the clock **MUST NOT** be translated. English path label is `Path`. `zh-Hant` path label is `路徑`.
8. `language` is not an argv verb.

### 2.1 Implementation Notes

| Field | Value |
|-------|--------|
| Class | `MenuLanguage` in `src/PyBackup/menu_language.py` |
| Env | `PYBACKUP_LANG` |
| Leaf | `~/.local/PyBackup/language` |

### 2.2 Code example

```python
class MenuLanguage:
    LEAF_NAME = "language"

    def leaf_path(self, home):
        return os.path.join(home, ".local", "PyBackup", self.LEAF_NAME)
```

The leaf is one token, mode 0600. A worked path shape is `~/.local/PyBackup/language`. Do not write a live login into this file.

```text
PYBACKUP_LANG=en py-backup help
```

## Terminologies

### Major TUI entry point

**Definition:** Major TUI entry point is the rule that the major entry of a claimed text screen is interactive mode with no positional command token. Flags that are not a command stay on that entry. `--json` with no command stays JSON help, not the text screen. A verb opens the screen only when a specialized requirement names that verb for the screen. This term does not choose the language leaf.

**Human daily-life explanation:** A major TUI entry point is the walk-up board. You see that board when you name no dish. The language board is a side room you open from that board. Naming `language` on the command line is not a dish this program accepts.

**Daily-life example:** You walk in with no extra words and see the front board. You open the language room and pick 41. You do not type `py-backup language`.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | Thirteen codes and the PyBackup leaf |
| 2026-10-22 | Active 1.0.1 | Leaf path sample. `language` stays off the command line. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
