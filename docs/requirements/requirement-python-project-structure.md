**file**: docs/requirements/requirement-python-project-structure.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-project-structure`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

Where the Python program lives in this tree, and where one run keeps its scratch folder.

Project nature: a command-line program. The program people run is `src/PyBackup`. The shell file stays beside it as a reference.

### 1.1 Human-facing

**In one sentence:** The command you run is the package under `src/PyBackup`, and each backup uses a private scratch folder named for you and this process.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Scratch is yours for this process, mode 0700 | `cache-PyBackup-{{USERNAME}}-<pid>` |
| The other role | The shell file is not the command | `src/folder-backup` |
| Not this file | How the archive is named and verified | The backup requirement |

| Includes | Excludes |
|----------|----------|
| Package path, test runners, scratch leaf, config, persistence | A home path of a live login |
| Parents: `TMPDIR`, then `/dev/shm`, then the temp directory | The shell cache path `/dev/shm/cache/cache-folder-backup-…` |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/PyBackup` | the package | the command |
| `tests/run.sh` | the Python suite | `py-backup` proofs |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Run the suite | `tests/run.sh` runs the Python tests. `tests/run-shell.sh` runs the shell reference. | `sh tests/run.sh` |

## 2. Core Rules (Mandatory)

1. Import package **MUST** be `src/PyBackup`. Entry is `python -m PyBackup` and the console script `py-backup`.
2. `src/folder-backup` and `src/folder-backup.sha256` **MUST** remain as the shell reference. They are not the `py-backup` command.
3. Tests for the Python command live in `tests/test_pybackup.py`. `tests/run.sh` runs that suite. `tests/run-shell.sh` runs the shell reference suite.
4. Scratch for a backup is not the repository. The leaf is `cache-PyBackup-<login>-<pid>`. `<login>` is `id -un` at runtime. Parents, in order: `TMPDIR` when set, then `/dev/shm` when it is a directory, then the process temp directory. The leaf mode is 0700.
5. Config drafts are `~/.config/PyBackup`. Persistence is `~/.local/PyBackup`.

### 2.1 Code example

```python
def scratch_leaf(login, pid):
    return "cache-PyBackup-{0}-{1}".format(login, pid)
```

Worked leaf: `cache-PyBackup-{{USERNAME}}-<pid>`. Do not write a live login or `/home/<login>` into this file.

```text
python -m PyBackup
py-backup version
```

## Terminologies

### Operational verb

**Definition:** An operational verb is a CLI routed-verb that runs the product. Backup and restore are operational verbs. Their steps live on the backup requirement. This file only names where the program and the scratch leaf sit.

**Human daily-life explanation:** The operational verb is the job. This file is the labeled drawer the job uses for scratch paper.

**Daily-life example:** You pack a folder. The scratch drawer is `cache-PyBackup-{{USERNAME}}-<pid>`, mode 0700, and it is thrown away when the verb ends.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | Package layout for `src/PyBackup` |
| 2026-10-22 | Active 1.0.1 | Worked scratch leaf and parent order. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
