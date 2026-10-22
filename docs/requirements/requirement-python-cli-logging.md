**file**: docs/requirements/requirement-python-cli-logging.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-cli-logging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

Logging uses ChronicleLogger. This file does not own the package floor. That floor is `requirement-python-packaging`. There is no logging mold. The nearest output mold is not this procedure.

Project nature: a command-line program with one status notebook per run.

### 1.1 Human-facing

**In one sentence:** Each run keeps one status notebook named PyBackup, and a text menu does not mix those lines onto the screen.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You open the menu and the notebook stays quiet on the screen | `py-backup` |
| The other role | View-log still writes a line before it shows the file | `read log path=<path>` |
| Not this file | The pip floor `ChronicleLogger>=1.3.1` | The packaging requirement |

| Includes | Excludes |
|----------|----------|
| One `ChronicleLogger(...)` inside `def main` | A second logger, or constructing it at import |
| Quiet when a text screen opens | A log line for each clock redraw |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/PyBackup/cli.py` | `def main` | the one construct |
| Row 31 | view-log | reads the log after the line is written |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the menu | The notebook is quiet on the screen because a text screen is open. The file may still receive lines. | `py-backup` |
| View the log | The program writes `read log path=<path>` before it shows the file. | Choose row 31, or the view-log action on that board |

## 2. Core Rules (Mandatory)

1. `def main` in `src/PyBackup/cli.py` **MUST** construct `ChronicleLogger(...)` by writing that statement inside `main`. The module **MUST NOT** construct it at import and **MUST NOT** re-export it. A function whose job is to return `ChronicleLogger(...)` is not the construct.
2. The log name **MUST** be `PyBackup`. A text-screen run (empty argv on a terminal, or `about` on a terminal) **MUST** pass `is_quiet=True` so the menu is not mixed with log lines on the screen. That quiet flag is chosen before the first product object.
3. View-log **MUST** log `read log path=<path>` and clear-log **MUST** log `clear log path=<path>`, component `menu`, level INFO, before the read and before the empty. Those calls **MUST NOT** sit inside an `isDebug()` guard.
4. A clock redraw **MUST NOT** be a log line. The menu does not start a thread for the clock, so this file does not add a thread-log line.
5. The dependency floor is `ChronicleLogger>=1.3.1`.
6. Archive stage, deposit, and stage delete do not call `log_message` today. That gap stays on the product review. This example does not mark those lines present.

### 2.1 Code example

```python
def main(argv=None):
    text_screen = opens_text_screen  # empty argv or about, and stdout is a terminal
    logger = ChronicleLogger(
        logname="PyBackup",
        is_quiet=text_screen,
    )
    app = Cli(logger)
    return app.run(argv)


def view_log(logger, path):
    logger.log_message(
        "read log path={0}".format(path),
        level="INFO",
        component="menu",
    )
```

The terminal answer itself is measured once in `requirement-python-cli-interface`. This file consumes that answer as `text_screen`.

## Terminologies

### Chronicle logger

**Definition:** Chronicle-logger is the one process status logger, library ChronicleLogger, that `def main` instantiates by writing the statement `ChronicleLogger(...)` inside that function, before any product object. It records status through `log_message`. The log folder is the one `logDir()` returns. Product code does not copy that folder ladder and does not type the path. Not `print`. Not a second logger.

**Human daily-life explanation:** A chronicle-logger is the one kitchen notebook. You do not start a second notebook. The guests in the dining room do not hear a line that the notebook keeps for the staff. The notebook already has a shelf. You ask where that shelf is.

**Daily-life example:** You open the menu. The dining room stays quiet. The notebook can still receive “read log path=…” when you ask to see the log.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | ChronicleLogger inside `def main` |
| 2026-10-22 | Active 1.0.1 | Construct sample. Quiet when a text screen opens. Archive file logs stay an open gap. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
