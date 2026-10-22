**file**: docs/requirements/requirement-python-packaging.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-packaging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

The installable unit is a setuptools package. Version **1.0.0** is the first Python release. It does not continue the shell number 1.26.0.

Project nature: a command-line program people install with pip for their own login.

### 1.1 Human-facing

**In one sentence:** You install PyBackup for yourself with `python -m pip`, then the command `py-backup` is on your path.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Install and refresh the package as yourself | `python -m pip install --user PyBackup` |
| The other role | An admin grant is not this install | No `sudo` on the pip line |
| Not this file | The verb list and the menu picture | The CLI and text-menu requirements |

| Includes | Excludes |
|----------|----------|
| `pyproject.toml`, version 1.0.0, console script | A `curl` pipe or `SCRIPT_URL` |
| Pip lifecycle commands | Shell `install` / `uninstall` as `py-backup` verbs |

| Surface | What you open | What for |
|---------|---------------|----------|
| `pyproject.toml` | the package manifest | name, version, script |
| `py-backup version` | the command | the installed version |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install | Pip places the console script for this login. It does not become root. | `python -m pip install --user PyBackup` |
| Check the copy | The printed version matches `__version__` and the manifest. | `py-backup version` |
| Refresh | The same pip program updates the distribution `PyBackup`. | `py-backup self-update` |
| Remove | The command line requires `--force`. Row 86 on the menu is the confirmation. | `py-backup self-uninstall --force` |

## 2. Core Rules (Mandatory)

1. `pyproject.toml` name **MUST** be `PyBackup`. Version **MUST** match `src/PyBackup/__init__.py` `__version__`.
2. `requires-python` **MUST** be `>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*`.
3. Dependency **MUST** include `ChronicleLogger>=1.3.1`.
4. Console script **MUST** be `py-backup = PyBackup.cli:main`.
5. Packages **MUST** be found under `src`.
6. License **MUST** be MIT. Author is cloudgen. Homepage is `https://github.com/cloudgen/PyBackup`.
7. There is no shell `SCRIPT_URL` on this package.
8. Editing this requirement does not bump product version 1.0.0.

### 2.1 Code example

```toml
[project]
name = "PyBackup"
version = "1.0.0"
requires-python = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"
dependencies = [
  "ChronicleLogger>=1.3.1",
]

[project.scripts]
py-backup = "PyBackup.cli:main"
```

```text
python -m pip install --user PyBackup
py-backup version
py-backup self-install
py-backup version-check
py-backup self-update
py-backup self-uninstall --force
```

## Terminologies

### Coding-style requirement

**Definition:** A coding-style requirement is the software-development specialize-in home for portable learned lessons about how the program is written. Without that file, agents bring portable learned lessons raw. This packaging file is not that style sheet. The style sheet is `requirement-python-coding-style`.

**Human daily-life explanation:** The style sheet is the newsroom’s adopted dates-and-names page. The package manifest is the label on the box you hand someone. They are different pages.

**Daily-life example:** The box says “PyBackup 1.0.0.” The style sheet says how the program inside the box is written.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | First Python package law. Product version 1.0.0. |
| 2026-10-22 | Active 1.0.1 | Manifest sample and pip place lines. Product version stays 1.0.0. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
