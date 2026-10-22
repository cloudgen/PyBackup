**file**: docs/requirements/requirement-python-error-handling.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-error-handling`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

Failures the operator can act on say what happened and the next step. They do not continue.

Project nature: a command-line program. This file is the failure sentence for that program.

### 1.1 Human-facing

**In one sentence:** When a pack or restore cannot finish, you see `ERROR:` and a `Next:` line you can type, and the program stops.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You read the two lines and type the next command | `py-backup help` |
| The other role | An admin grant does not replace this sentence | The JSON grant is a different file |
| Not this file | Menu drawing and archive naming | Those stay on their requirements |

| Includes | Excludes |
|----------|----------|
| `DomainError`, stderr `ERROR:` and `   Next:` | A second status notebook for the same sentence |
| Fail closed on Termux, Git Bash, and Windows cmd | Wrapping sudo on those hosts |

| Surface | What you open | What for |
|---------|---------------|----------|
| stderr | the two lines | what happened and the next command |
| `src/PyBackup/storage.py` | `DomainError` | the raised failure |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Read a failure | The first line says what stopped. The second line is a command or a path you can use. The program has already returned non-zero. | `py-backup backup /path/to/project` |

## 2. Core Rules (Mandatory)

1. Domain failures **MUST** raise `DomainError` with a message and a next step.
2. The command path **MUST** print `ERROR: <message>` and `   Next: <step>` on stderr and return non-zero.
3. A staged archive **MUST** be removed when backup ends, including the failure path.
4. Termux (`PREFIX` contains `com.termux` or `TERMUX_VERSION` is set), Git Bash (`MSYSTEM` is `MINGW*` or `MSYS*`), and Windows cmd (`OS=Windows_NT` and `COMSPEC` names `cmd.exe`, excluding Git Bash, Cygwin, and WSL) **MUST** fail backup and restore closed and **MUST NOT** call sudo.
5. Submit **MUST NOT** create the inbound directory. Generate **MUST** refuse a destination under `/etc` and under the inbound tree.
6. Restore **MUST** refuse `/`, FHS roots, `/etc/passwd`, and the deposit tree. `/etc/<login>` is allowed when the login is not `passwd`. A non-empty destination without `--force` **MUST** fail.
7. StateLogic is unordered on `requirement-python-oop`. This file does not add an `Attr` error counter.

### 2.1 Code example

```python
class DomainError(Exception):
    def __init__(self, message, nxt):
        Exception.__init__(self, message)
        self.message = message
        self.nxt = nxt

def report_error(message, nxt):
    print("ERROR: {0}".format(message), file=sys.stderr)
    print("   Next: {0}".format(nxt), file=sys.stderr)
    return 1
```

```text
ERROR: source folder is missing.
   Next: py-backup backup /path/to/project
```

## Terminologies

### Operator-readable error

**Definition:** An operator-readable error is a product failure message a person at the prompt can act on without decoding maintainer jargon. It states what happened in one concrete sentence, what it means in plain words, and what to do next (a command or who to ask). It is written concrete-first, with a next step, and it is not an incident breadcrumb.

**Human daily-life explanation:** An operator-readable error is a failure message a person at the prompt can act on: what happened, what it means, what to do next, without maintainer slang.

**Daily-life example:** “The oven is off; turn the knob to 180 and press Start” beats “E_THERM_NULL in module 7.”

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | First Python failure sentences |
| 2026-10-22 | Active 1.0.1 | `DomainError` and `report_error` sample. StateLogic stays unordered. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
