**file**: docs/requirements/requirement-python-cli-interface.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-cli-interface`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

This file owns the `py-backup` command: which words are verbs, what an empty argument list does, and how help is split. The text menu picture is `requirement-python-tui`. Backup steps are `requirement-folder-archive-backup`. The JSON grant body is `requirement-sudoer-json-file`.

Project nature: a command-line program that packs and restores one login’s folders.

### 1.1 Human-facing

**In one sentence:** You type `py-backup` with no extra words on a terminal and the numbered menu opens; the same empty line off a terminal prints help and stops.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Run the command as yourself | `py-backup help` |
| The other role | An admin who later installs a grant is not this file | The grant body is the JSON requirement |
| Not this file | Packing steps, the menu drawing, and the JSON body | Those stay on their own requirements |

| Includes | Excludes |
|----------|----------|
| Verb list, empty-argument behavior, help headings | Drawing the box, tar rules, sudoers JSON fields |
| One terminal check stored before dispatch | Calling `input()` or measuring the terminal again inside a helper |

| Surface | What you open | What for |
|---------|---------------|----------|
| `py-backup` | the command | menu or help |
| `src/PyBackup/cli.py` | the program file | dispatch |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the menu | On a terminal, no extra words opens the front board. It does not install a package. | `py-backup` |
| Pack a folder | The backup verb needs a folder. Off a terminal, a missing folder fails closed. | `py-backup backup /path/to/project` |
| Read help | Help lists work commands, then the grant and draft commands used for tests and review. | `py-backup help` |

## 2. Core Rules (Mandatory)

1. Console script **MUST** be `py-backup = PyBackup.cli:main`. `def main` **MUST** live in `src/PyBackup/cli.py` and **MUST** construct `ChronicleLogger` inside `main`, not at import.
2. Empty argv on a terminal **MUST** open the front board and **MUST NOT** run pip and **MUST NOT** show a welcome line. Empty argv off a terminal **MUST** print help and return 0.
3. Whether stdout is a terminal **MUST** be measured once in `run` before dispatch. Later steps **MUST** use that stored answer. They **MUST NOT** call `isatty` again.
4. `help`, `-h`, and `--version` **MUST NOT** open the screen. `about` on a terminal **MUST** open the about result page. `version` **MUST** print the version and **MUST NOT** call pip.
5. Work verbs: `backup`, `restore`, `remove-project-sudoers`, `submit-sudoer-request`. Test-purpose verbs: `print-sudoers`, `print-sudoers-install-script`, `generate-sudoer-request`. Lifecycle verbs: `version-check`, `self-update`, `self-install`, `self-uninstall`. `help`, `version`, and `about` stay typed.
6. `sudoers` **MUST NOT** be a dispatched command. `hello` **MUST NOT** be a verb.
7. Each work-menu token **MUST** also be an argv verb. Exit is not an argv verb. `help` is usage and is not a numbered row.
8. When `backup` or `restore` lacks its operand and stdout is a terminal, the program **MUST** ask in the text-menu box and **MUST NOT** call `input()`. Off a terminal it **MUST** fail closed and **MUST NOT** prompt.
9. English help **MUST** use the headings `Work commands:` then `Grant and draft setup (tests and review):` in that order. Other codes translate those headings and keep the split. Command tokens stay Latin.
10. `--force` is allowed for `self-uninstall` (required on the command line), `restore`, and `remove-project-sudoers`. `--json` is a global flag before the verb. Restore also accepts `--disk` and `--ram`. Generate and submit accept `--add`, `--update`, `--allow-test-local`, and `--purpose`.
11. Pip verbs **MUST** run `python -m pip` with distribution `PyBackup`. They **MUST NOT** use `sudo` or `curl`. Command-line `self-uninstall` **MUST** require `--force`. Choosing row 86 on the menu is the confirmation.
12. An unknown verb **MUST** return non-zero with `ERROR:` and `Next:`.
13. Operator errors **MUST** be `ERROR: …` and `   Next: …` on stderr.
14. Who may run a verb stays the class residual already recorded: considered, no dest approver. This file does not add a second who-table.

### 2.1 Implementation Notes

| Field | Value |
|-------|--------|
| Command | `py-backup` |
| Basic usage | `py-backup backup /path/to/project` |
| Homepage | `https://github.com/cloudgen/PyBackup` |
| Author | cloudgen |

### 2.2 Code example

The terminal answer is stored once. Helpers consume `on_terminal`.

```python
class Cli:
    CONSOLE_NAME = "py-backup"

    @staticmethod
    def stdout_is_tty():
        try:
            return sys.stdout.isatty()
        except Exception:
            return False

    def run(self, argv):
        on_terminal = self.stdout_is_tty()
        if not argv:
            if on_terminal:
                return self.open_menu()
            self.write_help()
            return 0
        if argv[0] == "backup":
            return self.backup(argv[1:])
        return self.report_error(
            "Unknown verb '{0}'.".format(argv[0]),
            "py-backup help",
        )
```

```text
py-backup
py-backup help
py-backup version
py-backup about
py-backup backup /path/to/project
py-backup restore alpha --disk
py-backup remove-project-sudoers --force
py-backup submit-sudoer-request
py-backup print-sudoers
py-backup print-sudoers-install-script --allow-test-local
py-backup generate-sudoer-request --allow-test-local
py-backup self-install
py-backup version-check
py-backup self-update
py-backup self-uninstall --force
```

The same lines are repeated on the requirement that owns each verb. Help text is not that second mention.

## 3. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Empty argv off a terminal is help and status 0 |
| AC-2 | `hello` and `sudoers` are not verbs |
| AC-3 | Help heading order is work, then grant and draft setup |
| AC-4 | Pip argv contains `python -m pip` and does not contain curl or sudo |
| AC-5 | `run` stores the terminal answer once before dispatch |

## Terminologies

### Operational verb

**Definition:** An operational verb is a CLI routed-verb that runs the product: lifecycle (install, help), domain convert/submit/list/show, dest emit, admin setup/review, or other live host or queue work. It is not a test-purpose verb. Who may run it still applies. An ordinary-login operational verb such as submit or convert stays distinct from an ordinary-login unit tester.

**Human daily-life explanation:** An operational verb is a command that actually does product work: install, help, convert, submit, list. It is not a unit-test-only verb.

**Daily-life example:** “Please bake the cake” is operational; “please run the kitchen’s practice quiz about baking” is a test verb.

### Test-purpose verb

**Definition:** A test-purpose verb is a CLI routed-verb whose only job is a unit test of product functions. Its target is a local test folder. If that folder or its files need a mode or owner, in-tool elevation must go through the one sudo-wrapping function and must check before sudo. Other than that wrap, it must not use sudo. It must not submit, queue, write a dest, set up, approve, or take other operational-verb steps.

**Human daily-life explanation:** A test-purpose verb is a practice drill whose only job is to exercise a function on a local sample folder. It is not mailing, not approving, and not rewriting the building.

**Daily-life example:** “Quiz the doorbell on the cardboard mock-up in the garage.” That quiz is not ringing the real street doorbell.

## 4. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | First Python command law for `py-backup` |
| 2026-10-22 | Active 1.0.1 | Code example stores the terminal answer once. Invocation lines for every routed verb. `--purpose` is listed. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
