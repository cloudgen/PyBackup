**file**: docs/requirements/requirement-python-cli-storage.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-cli-storage`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

This file is where `py-backup` keeps a scratch folder for one run, and where this login keeps notes that survive a reboot. The deposit tree `/var/backup/PyBackup/` is not either of those folders.

Project nature: a command-line program. Scratch is private to this login and this process.

### 1.1 Human-facing

**In one sentence:** `py-backup about` names the scratch folder this run is using, the preferred folder, two fallbacks, and the persistence folder under `~/.local/PyBackup`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Scratch is yours for this process, mode 0700 | `cache-PyBackup-<login>-<pid>` |
| The other role | The deposit tree is the shared host store | `/var/backup/PyBackup/` |
| Not this file | How the archive is named | `requirement-python-idempotency` |

| Includes | Excludes |
|----------|----------|
| Scratch parents, persistence, config drafts, the language leaf | A home path of a live login |
| Quiet skip when a parent cannot be used | A warning because a higher folder was skipped |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/PyBackup/storage.py` | `resolve_storage` | the scratch leaf |
| `py-backup about` | the cache lines | used, preferred, 1st, 2nd, persistence |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Read the cache lines | About names the folder in use. A parent that cannot be used is skipped with no extra line. | `py-backup about` |

## 2. Core Rules (Mandatory)

1. Scratch **MUST** be `cache-PyBackup-<login>-<pid>`. `<login>` is the invoking login at runtime (`id -un`). `<pid>` is this process. The leaf mode **MUST** be 0700. Two logins **MUST NOT** share one leaf.
2. Parents, in order, **MUST** be `TMPDIR` when it is set, then `/dev/shm` when it is a directory, then the process temp directory. A parent that cannot be created or written **MUST** be skipped. When every parent fails, backup **MUST** stop with `ERROR:` and a next step.
3. Persistence **MUST** be `~/.local/PyBackup`. Config drafts **MUST** be `~/.config/PyBackup`. Neither folder is the deposit tree and neither is `~/.local/bin`.
4. The language leaf **MUST** be `~/.local/PyBackup/language`, mode 0600. Its directory mode is 0700. It **MUST NOT** live in the scratch folder and **MUST NOT** live under `/var/backup`. `PYBACKUP_LANG` wins for one run and **MUST NOT** write that leaf. Codes stay on `requirement-python-cli-language`.
5. About **MUST** print these English labels: `Cache folder used`, `Cache folder preferred`, `Cache folder 1st`, `Cache folder 2nd`, `Persistence storage`. A miss prints `unavailable` for the used folder. Preferred is `TMPDIR` when set, otherwise `/dev/shm`.
6. The stage file inside the scratch folder **MUST** be mode 0600. The leaf name **MUST NOT** be `cache-folder-backup`.

### 2.1 Code example

```python
def scratch_leaf(login, pid):
    return "cache-PyBackup-{0}-{1}".format(login, pid)

def scratch_parents():
    parents = []
    if os.environ.get("TMPDIR"):
        parents.append(os.environ["TMPDIR"])
    if os.path.isdir("/dev/shm"):
        parents.append("/dev/shm")
    parents.append(tempfile.gettempdir() or "/tmp")
    return parents
```

## Terminologies

### Scratch folder

**Definition:** A scratch folder is a mode 0700 directory for one login and one process. `py-backup` stages an archive there and removes that stage when the run ends. It is not the deposit tree.

**Human daily-life explanation:** The workbench is yours for this job. The finished package goes to the shared shelf. The workbench is cleared when the job ends.

**Daily-life example:** The leaf `cache-PyBackup-<login>-<pid>` holds the stage. `/var/backup/PyBackup/` holds the deposited archive.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-23 | Active 1.0.0 | Python storage for `py-backup`. Scratch order is TMPDIR, `/dev/shm`, then the temp directory. |

**Last Updated**: 2026-10-23
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
