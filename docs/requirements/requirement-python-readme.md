**file**: docs/requirements/requirement-python-readme.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-readme`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

The product README is the user document for `py-backup`. It is not the shell 1.26.0 document.

Project nature: a command-line program. The README is the page a person reads before they install.

### 1.1 Human-facing

**In one sentence:** The root README names PyBackup 1.0.0, tells you to install with pip, and shows the menu rows 1, 3, 4, 5, 8, and 9.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You follow the install line and then run the command | `python -m pip install --user PyBackup` |
| The other role | The shell 1.26.0 document is not this page | `src/folder-backup` stays a reference |
| Not this file | The law of each verb | The requirement that owns that verb |

| Includes | Excludes |
|----------|----------|
| Name, version, pip install, menu text fence | A `curl` pipe as the lead install |
| Clock sample `HH:MM:SS` and “current directory” | A home path in the menu fence |

| Surface | What you open | What for |
|---------|---------------|----------|
| `README.md` | the user page | install and menu picture |
| `py-backup help` | the command | the same verbs, in the program |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install from the page | Pip, as yourself. The page does not ask you to pipe a downloaded script. | `python -m pip install --user PyBackup` |
| Read help | The program lists the commands. The README does not invent extra front rows. | `py-backup help` |

## 2. Core Rules (Mandatory)

1. Root `README.md` **MUST** name PyBackup, version 1.0.0, and the command `py-backup`.
2. Quick Installation **MUST** be `python -m pip`. It **MUST NOT** lead with `curl | sh`.
3. The main-menu capture **MUST** show rows 1, 3, 4, 5, 8, and 9, and **MUST** include the client, sudoers, system-log, language, and self-management boards that this menu opens.
4. The capture **MUST NOT** list install, version, about, help, or the three test-purpose verbs as front rows.
5. Pictures that are also the package description use an absolute `https` URL. This release’s menu capture is a text fence of the painter’s rows. The clock sample is local time. The directory is described as the current directory and is not a home path.

### 2.1 Code example

```text
python -m pip install --user PyBackup
py-backup
py-backup help
py-backup backup /path/to/project
```

The menu fence in the README uses the current directory and clock `HH:MM:SS`. It does not paste a home path.

## Terminologies

### Test-purpose verb

**Definition:** A test-purpose verb is a CLI routed-verb whose only job is a unit test or a draft the operator types for review. On this product those tokens are `print-sudoers`, `print-sudoers-install-script`, and `generate-sudoer-request`. They are not front-menu rows.

**Human daily-life explanation:** A practice drill stays off the front chalkboard. You can still type it.

**Daily-life example:** The README chalkboard shows rooms 1, 3, 4, 5, 8, and 9. It does not paint `generate-sudoer-request` as a front room.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | README shape for PyBackup 1.0.0 |
| 2026-10-22 | Active 1.0.1 | Usage fence sample. Help is named here as well as on the CLI requirement. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
