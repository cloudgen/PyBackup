**file**: docs/requirements/requirement-python-idempotency.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-idempotency`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

This file is re-run safety for `py-backup`. A second backup the same day adds the next archive number. It does not replace the archive already deposited.

Project nature: a command-line program. Backup is additive. Read-only commands are safe to repeat.

### 1.1 Human-facing

**In one sentence:** Pack the same folder twice today and the second file is `NAME-YYYYMMDD-2.tar.gz`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You run backup again | `py-backup backup /path/to/project` |
| The other role | A script may repeat a read-only command | `py-backup version` |
| Not this file | How many archives to keep | The retention requirements |

| Includes | Excludes |
|----------|----------|
| Next free `N`, starting at 1 | Overwriting `NAME-YYYYMMDD-1.tar.gz` |
| A stop when no free `N` remains | A success that clobbers an existing archive |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/PyBackup/archive.py` | `next_archive_name` | the next free name |
| The deposit tree | `SOURCE-YYYYMMDD-N.tar.gz` | the file that must stay |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Pack twice | The first deposit keeps `N` 1. The second deposit uses the next free `N`. | `py-backup backup /path/to/project` |

## 2. Core Rules (Mandatory)

1. An archive name **MUST** be `SOURCE-YYYYMMDD-N.tar.gz`. `N` **MUST** start at 1. The chosen name **MUST NOT** already exist in the deposit directory.
2. A second backup **MUST NOT** skip the deposit because an archive already exists. It **MUST** allocate the next free positive `N`. When no `N` through 9999 is free, backup **MUST** stop with `ERROR:` and a next step.
3. Default backup **MUST NOT** overwrite an existing archive. There is no force flag that replaces a deposited name.
4. `version`, `about`, `help`, and `print-sudoers` **MUST** be safe to repeat. `generate-sudoer-request` **MAY** overwrite the same local draft. It **MUST NOT** write `/etc`.
5. Each successful `submit-sudoer-request` is a new queue item. A missing inbound directory **MUST** fail closed and **MUST NOT** be created by this command.
6. Restore of a non-empty destination **MUST** fail unless `--force` is set. `--force` **MUST NOT** skip the destination whitelist.
7. Termux, Git Bash, and Windows cmd **MUST** fail backup and restore closed. Re-run safety **MUST NOT** call sudo to force a deposit on that class.
8. Retention after a successful deposit stays on the daily and total retention requirements. Idempotency does not mean “never error” on a bad path.

### 2.1 Code example

```python
def next_archive_name(source_name, day, taken):
    n = 1
    while n <= 9999:
        name = "{0}-{1}-{2}.tar.gz".format(source_name, day, n)
        if name not in taken:
            return name
        n += 1
    raise DomainError(
        "Could not allocate archive name.",
        "py-backup help",
    )
```

## Terminologies

### Next archive number

**Definition:** The next archive number is the smallest positive integer `N` such that `SOURCE-YYYYMMDD-N.tar.gz` is not already in the deposit directory.

**Human daily-life explanation:** Today’s first parcel is number 1. The next parcel gets the next free number. You do not paste a new label over yesterday’s parcel.

**Daily-life example:** `alpha-20261023-1.tar.gz` stays. The next pack of `alpha` that day is `alpha-20261023-2.tar.gz`.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-23 | Active 1.0.0 | Python re-run safety for `py-backup`. Next `N` does not overwrite. |

**Last Updated**: 2026-10-23
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
