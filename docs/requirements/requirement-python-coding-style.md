**file**: docs/requirements/requirement-python-coding-style.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-coding-style`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

Style for the Python program in `src/PyBackup`. Without this requirement, portable learned lessons arrive raw and get treated as this product’s law. The shell file `src/folder-backup` keeps `requirement-shell-script-coding`.

Project nature: a command-line program. This file is the adopted writing sheet for that program.

### 1.1 Human-facing

**In one sentence:** This file says how the Python program is written, and it points packing rules at the backup requirement instead of copying them.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You read the style when you change `src/PyBackup` | A stage file is mode 0600 |
| The other role | The shell file keeps its own style sheet | `src/folder-backup` |
| Not this file | Class homes, the verb list, and tar member rules | Those requirements own those topics |

| Includes | Excludes |
|----------|----------|
| Specialize-in intention, stage mode 0600, `ClassName(...)` at the site | A second copy of cache parents, symlink rules, or tar `-h` |
| A pointer to the backup requirement for those rules | A function whose only job is to return `Cli(...)` |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/PyBackup` | the program | the style this file adopts |
| `requirement-folder-archive-backup` | backup law | cache, symlinks, tar |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Seal a stage | The staged archive is mode 0600 before it is copied. The backup requirement owns where that file lives. | `py-backup backup /path/to/project` |

## 2. Core Rules (Mandatory)

1. New modules use the class homes in `requirement-python-oop`. The site that needs an object writes `ClassName(...)`. A function that returns `Cli(...)` is a factory and is not this style.
2. A public function states its job in a short docstring when the name does not already say it.
3. The staged archive mode is 0600. Cache parents, the leaf name, symlink follow, and tar `-h` stay on `requirement-folder-archive-backup` and `requirement-python-project-structure`. This file points there.
4. Publish a deposit with a copy into the destination. Do not leave the stage as the published file. The copy steps stay on `requirement-folder-archive-backup`.
5. Comments cite live `requirement-*.md` keys, not skills or templates.
6. No unfinished markers in the package.
7. In-tool sudo, when it exists, is studied on `requirement-shell-sudo-command`. This file does not keep a second wrap body.

### 2.1 Code example

```python
def seal_stage(path):
    """Stage archive is mode 0600. Parents stay on the backup requirement."""
    os.chmod(path, 0o600)


def main(argv=None):
    logger = ChronicleLogger(logname="PyBackup", is_quiet=False)
    app = Cli(logger)
    return app.run(argv)
```

`Cli(logger)` is the construct. `def make_cli(logger): return Cli(logger)` is not the sample.

## Terminologies

### Coding-style requirement

**Definition:** A coding-style requirement is the software-development specialize-in home for portable learned lessons about how the program is written. Every software-development project must have an Active language-matched coding-style requirement. Without that file, agents bring portable learned lessons raw and treat them as this product’s law. The coding-style requirement is where those lessons are adopted, pointed at peer requirements, or refused.

**Human daily-life explanation:** A coding-style requirement is this product’s adopted writing style home. Every software-development project must have one. Without it, helpers would treat portable lessons as this product’s law raw. The requirement is where those lessons are taken, pointed, or refused.

**Daily-life example:** A newsroom keeps one style sheet (“we write dates this way”). That adopted sheet is the coding-style requirement. The industry handbook on the shelf is not house law until the sheet says so.

### Avoid-factory-create-class

**Definition:** Avoid-factory-create-class is the portable Python construct rule that an object is created by writing `ClassName(...)` at the site that needs that object. A factory is a function or a method whose job is to instantiate a class: a module function that returns `SomeClass(...)`, a method that returns `SomeClass(...)`, or `Cls.__new__(Cls)` followed by a method that builds the object. The class can be created without that factory. The factory does not add a way to create the object that the call site lacks. It hides the class name behind a second home.

**Human daily-life explanation:** Avoid-factory-create-class means you pick up the thing itself. You do not hand the job to a clerk whose only task is to pick it up and hand it back. The class already knows how to become an object. Writing `ClassName(...)` is that step. A factory is the clerk.

**Daily-life example:** You want a kettle. You take a kettle off the shelf. You do not fill out a slip that a back-room clerk uses to fetch the same kettle and pass it through a window.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | First Python style sheet |
| 2026-10-22 | Active 1.0.1 | Specialize-in sentence. Stage seal sample. Cache and symlink rules point at the backup requirement. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
