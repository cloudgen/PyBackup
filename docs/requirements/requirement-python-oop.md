**file**: docs/requirements/requirement-python-oop.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-oop`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

Name the class that owns each job so a second painter or a second logger is not added beside it. StateLogic stays unordered. The site that needs an object writes `ClassName(...)`.

Project nature: a command-line program with one class per job.

### 1.1 Human-facing

**In one sentence:** Each job in PyBackup has one named class, and `def main` in `cli.py` builds `Cli` by writing `Cli(...)`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You run `py-backup`; the program builds `Cli` inside `main` | `py-backup version` |
| The other role | Domain packing is not folded into `Cli` | `archive.py` |
| Not this file | Verb lists, menu ink, and the package manifest | Those requirements |

| Includes | Excludes |
|----------|----------|
| The class table and `Cli(logger)` at the site | A factory function that returns `Cli(...)` |
| StateLogic left unordered | An `Attr` block added only to match a mold |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/PyBackup/cli.py` | `def main` | constructs `Cli` |
| `src/PyBackup/*.py` | one class per module | the table below |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start the program | `main` writes `ChronicleLogger(...)` and then `Cli(logger)`. No helper returns that `Cli`. | `py-backup` |

## 2. Core Rules (Mandatory)

| Class | Module | Owns |
|-------|--------|------|
| `Cli` | `cli.py` | Parse, dispatch, help, tty gate. `def main` stays in this file |
| `Tui` | `tui.py` | Session loop and menu questions |
| `MenuPainter` | `menu_painter.py` | Frame, columns, band, path line |
| `MenuModel` | `menu_model.py` | Keystroke state and which board is open |
| `MenuSession` | `menu_session.py` | Clock wait and action dispatch |
| `MenuLanguage` | `menu_language.py` | Codes, leaf, sentences |
| `AboutPage` | `about_page.py` | About text |
| `CheckSystem` | `check_system.py` | Host check lines |
| `SelfManage` | `self_management.py` | Pip argv |
| `SystemLog` | `system_log.py` | Log folder, list, clear |
| `DomainError` | `storage.py` | Operator failure |
| Settings and archive functions | `archive.py` | Backup, restore, retention, about fields |
| Grant functions | `sudoers.py` | JSON grant, text dual, submit, remove draft |

Domain code **MUST NOT** be folded into `Cli`. Pip code **MUST NOT** be folded into the archive module.

The console script stays `PyBackup.cli:main`. A function whose job is to return `Cli(...)` is a factory and is not the construct.

### 2.1 Code example

```python
def main(argv=None):
    logger = ChronicleLogger(
        logname="PyBackup",
        is_quiet=False,
    )
    app = Cli(logger)
    return app.run(argv)
```

Quiet for a text screen is decided in `requirement-python-cli-logging`. This sample only shows the construct. It does not add StateLogic.

## Terminologies

### Avoid-factory-create-class

**Definition:** Avoid-factory-create-class is the portable Python construct rule that an object is created by writing `ClassName(...)` at the site that needs that object. A factory is a function or a method whose job is to instantiate a class: a module function that returns `SomeClass(...)`, a method that returns `SomeClass(...)`, or `Cls.__new__(Cls)` followed by a method that builds the object. The class can be created without that factory. The factory does not add a way to create the object that the call site lacks. It hides the class name behind a second home.

**Human daily-life explanation:** Avoid-factory-create-class means you pick up the thing itself. You do not hand the job to a clerk whose only task is to pick it up and hand it back.

**Daily-life example:** You want a kettle. You take a kettle off the shelf. You do not fill out a slip that a back-room clerk uses to fetch the same kettle and pass it through a window.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | Class table for the Python program |
| 2026-10-22 | Active 1.0.1 | `Cli(logger)` sample. StateLogic stays unordered. A factory is not the sample. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
