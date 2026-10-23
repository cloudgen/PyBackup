**file**: docs/requirements/requirement-python-cli-default-interaction.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-cli-default-interaction`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

This file is how `py-backup` behaves when you give it no command, and how a numbered board returns. The picture of the rows stays on `requirement-python-tui`. The verb list stays on `requirement-python-cli-interface`.

Project nature: a command-line program. An empty line on a terminal is the text menu. An empty line off a terminal is help.

### 1.1 Human-facing

**In one sentence:** On a terminal, `py-backup` with no command opens the numbered menu; off a terminal it prints help and returns 0.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You open the menu and pick a number | `py-backup` |
| The other role | A script with no command must not wait on the menu | `py-backup` with no terminal |
| Not this file | The paint of each row and the packing steps | `requirement-python-tui` and the backup requirement |

| Includes | Excludes |
|----------|----------|
| Empty argv, Back **0**, Exit **9**, return to the front after a leaf | A `menu` or `main` command |
| `sudoers` refused as a typed command | A pipe that installs the program |

| Surface | What you open | What for |
|---------|---------------|----------|
| `py-backup` | the front board on a terminal | client-side, system-log, language, sudoers, self-management, Exit |
| `py-backup help` | the command list | the same verbs, off the menu |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the menu | A terminal with no command draws the front board. | `py-backup` |
| Step back | **0** on a child board returns to the front. **9** leaves with no confirm. | Choose 0, then 9 |

## 2. Core Rules (Mandatory)

1. Empty argv on a terminal **MUST** open the text menu and **MUST** return 0 when the operator picks Exit. Empty argv off a terminal **MUST** print help and return 0. It **MUST NOT** install or update.
2. `menu` and `main` are not commands. `sudoers` **MUST** fail with `sudoers is a menu, not a command.` The next step is `py-backup`.
3. Front rows, child rows, and the two not-available sentences stay on `requirement-python-tui`. This file does not renumber them. Row **2** stays unprinted.
4. **0** Back on a child board **MUST** return to the front board. It **MUST NOT** leave the program.
5. **9** Exit **MUST** return 0 with no confirm. Esc on a child board or a result page **MUST** return to the front and **MUST NOT** be Exit.
6. A finished leaf command **MUST** show its result and then the front board. It **MUST NOT** close the program.
7. An unknown token **MUST** stay on the current board. End of input on the front board **MUST** leave. The one-second clock wait is not end of input.
8. Self-management rows **MUST** use `python -m pip`. They **MUST NOT** call sudo and **MUST NOT** use curl.

### 2.1 Code example

```python
def run(self, argv):
    if not argv:
        if self.stdout_is_tty():
            return self.open_menu()
        self.write_help()
        return 0
    if argv[0] == "sudoers":
        return self.report_error(
            "sudoers is a menu, not a command.",
            "py-backup",
        )
    return self.dispatch(argv)
```

## Terminologies

### Zero-cli-verb

**Definition:** A zero-cli-verb is a run with no command word after the program name. On a terminal it opens the numbered menu. Off a terminal it prints help and returns 0.

**Human daily-life explanation:** You open the program and do not name a job. At the screen you get the menu. In a script you get the instructions and the script continues.

**Daily-life example:** `py-backup` at a prompt shows the front board. The same line in a pipeline prints help.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-23 | Active 1.0.0 | Python default interaction for `py-backup`. Rows stay on `requirement-python-tui`. |

**Last Updated**: 2026-10-23
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
