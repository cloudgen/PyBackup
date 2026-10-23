**file**: docs/requirements/requirement-python-sudo-command.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-sudo-command`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

This file is the in-tool sudo rule for `py-backup`. The JSON grant body stays on `requirement-sudoer-json-file`. The program does not write `/etc`.

Project nature: a command-line program. A normal login copies into the deposit tree only when that directory is writable, or when `sudo -n` can perform that copy after an admin has installed a grant.

### 1.1 Human-facing

**In one sentence:** After an admin installs the fragment, deposit may use `sudo -n` for the copy into `/var/backup/PyBackup/`. This login does not write `/etc`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You pack a folder. A writable deposit needs no sudo. | `py-backup backup /path/to/project` |
| Admin | Install `/etc/sudoers.d/PyBackup-<login>` after review | `visudo -c`, mode 0440 |
| Not this file | The four JSON command objects | `requirement-sudoer-json-file` |

| Includes | Excludes |
|----------|----------|
| Check writable first, then `sudo -n` for the deposit copy | `sudo true` as a probe |
| Fail closed on Termux, Git Bash, and Windows cmd | A grant that names `mkdir` or `cp` |

| Surface | What you open | What for |
|---------|---------------|----------|
| `py-backup print-sudoers` | four NOPASSWD lines | `backup *`, `restore *`, and the `--json` twins |
| `src/PyBackup/archive.py` | `_deposit` | the copy, with sudo only when needed |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Print the lines | The text names `py-backup` and the four argument lists. | `py-backup print-sudoers` |
| Pack when the deposit is not writable | The copy uses `sudo -n`. A refused sudo stops with `ERROR:` and a next step. | `py-backup backup /path/to/project` |

## 2. Core Rules (Mandatory)

1. Deposit **MUST** copy without sudo when the effective uid is 0 or the deposit directory is writable. It **MUST NOT** call sudo in that case.
2. Termux, Git Bash, and Windows cmd **MUST** fail backup and restore closed before any sudo call.
3. When sudo is required, the call **MUST** be `sudo -n`. A missing `sudo` or a non-zero status **MUST** stop with `ERROR:` and a next step of `py-backup print-sudoers`. The program **MUST NOT** prompt for a password.
4. The program **MUST NOT** probe with `sudo true`, `sudo ls`, or `sudo mkdir` before the real copy. It **MUST NOT** write `/etc`.
5. `print-sudoers` **MUST** list only these four NOPASSWD lines for `${GLOBAL_BIN}/py-backup` (default `/usr/local/bin/py-backup`): `backup *`, `restore *`, `--json backup *`, `--json restore *`. `<login>` is `id -un` and **MUST NOT** be frozen in this file.
6. The fragment name the program prints **MUST** be `/etc/sudoers.d/PyBackup-<login>`. OS-tool paths (`mkdir`, `install`, `cp`, `chmod`, `tar`, `rm`) **MUST NOT** appear in that grant.
7. The live deposit path still calls `sudo -n` for `mkdir`, `install` or `cp`, and `chmod` when the directory is not writable. Those calls are **Gap**: they are not the four grant lines in rule 5. This file **MUST NOT** mark that inner wrap Implemented.
8. Self-management **MUST NOT** call sudo. `remove-project-sudoers` deletes a local draft only.

### 2.1 Studied allow table

| Binary | Arguments | Fragment | NOPASSWD | Re-exec this program? |
|--------|-----------|----------|----------|------------------------|
| `${GLOBAL_BIN}/py-backup` | `backup *` | `/etc/sudoers.d/PyBackup-<login>` | yes | no |
| same | `restore *` | same | yes | no |
| same | `--json backup *` | same | yes | no |
| same | `--json restore *` | same | yes | no |

### 2.2 Code example

```python
def grant_commands(path):
    rows = (
        ["backup", "*"],
        ["restore", "*"],
        ["--json", "backup", "*"],
        ["--json", "restore", "*"],
    )
    return [
        {"runas": "root", "tags": ["NOPASSWD"], "path": path, "args": list(args)}
        for args in rows
    ]
```

## Terminologies

### Studied sudo allow table

**Definition:** A studied sudo allow table is the list of argv lines this program is willing to name in `print-sudoers`. For `py-backup` that list is four command objects. It is not a guess and it does not include OS-tool paths.

**Human daily-life explanation:** The note you hand an admin names exactly four jobs. It does not hand over the whole toolbox.

**Daily-life example:** The four lines are `backup *`, `restore *`, and the same two with `--json` in front.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-23 | Active 1.0.0 | Python sudo rule for `py-backup`. Inner `sudo -n` on deposit tools stays Gap. |

**Last Updated**: 2026-10-23
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
