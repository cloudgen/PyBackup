# PyBackup - Pack a folder into a dated gzip archive from a text menu

![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--engineered)-purple.svg)](https://github.com/cloudgen/ciao)
[![Stars](https://img.shields.io/github/stars/cloudgen/PyBackup?style=flat-square)](https://github.com/cloudgen/PyBackup)
[![Python](https://img.shields.io/badge/Python-2.7%20%7C%203.5%2B-blue?style=flat-square)](https://www.python.org/)

**PyBackup** packs a folder you name into a dated gzip archive under `/var/backup/PyBackup/`, checks the member count and the regular-file count, and can put that folder back onto the hard-disk projects tree. On a terminal with no command it opens a text menu. Off a terminal with no command it prints help and stops.

| You (your own login) | Admin / already root | Not this |
|----------------------|----------------------|----------|
| Install with pip, write a grant you can read, submit it, then run backup and restore after an admin has installed the grant | Install the package into a shared prefix and install the sudoers fragment | A normal login does not write `/etc`. A bare run does not download a shell script. |

| Includes | Excludes |
|----------|----------|
| Text menu, backup and restore, a JSON grant you can read, pip install / update / remove | A host service, a shell `curl \| sh` installer, writing `/etc` from this login |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install | Places the `py-backup` command for this login from a checkout. | `python -m pip install --user -e .` |
| Open the menu | On a terminal, a bare run shows client-side, system-log, language, sudoers, self-management, and Exit. Server-side is not available. | `py-backup` |
| Pack a folder | Copies the archive into `/var/backup/PyBackup/` when that directory is writable, or asks sudo only for the deposit when it is not. | `py-backup backup /path/to/project` |

## Features

- **Text menu.** On a terminal, `py-backup` with no command shows numbered rows and a rounded box along the bottom. The first row is the current directory and a local clock. The status line shows the name and the version.
- **Client-side.** **1** opens **11** backup and **12** restore.
- **System log.** **3** opens **31** view-log, **32** clear-log, and **33** log-folder.
- **Language.** **4** opens codes **41** through **53**. The saved choice is `~/.local/PyBackup/language`. `PYBACKUP_LANG` wins for one run and does not write that file.
- **Sudoers.** **5** opens **52** submit-sudoer-request and **55** remove-project-sudoers. Numbers **51**, **53**, and **54** stay reserved. The three test commands are typed, not numbered.
- **Self-management.** **8** opens **82** version, **83** about, **84** version-check, **85** self-update, **86** self-uninstall, and **87** self-install. Those pip commands are `python -m pip`. They do not use sudo and they do not use curl.
- **Exit.** **9** leaves. **0** on a child board steps back.
- **Backup.** Name `SOURCE-YYYYMMDD-N.tar.gz`. N starts at 1 and does not overwrite. A symlink is stored and is not counted as a regular file. After a successful deposit, keep at most 5 archives from the same day and 30 in total.
- **Restore.** The default destination is the hard-disk projects tree. `--force` is required when that folder is not empty. `/etc/<your-login>` is allowed. `/etc/passwd`, `/`, and the deposit tree are refused.
- **Grant you can read.** `generate-sudoer-request` writes four command objects: `backup *`, `restore *`, and the `--json` twins. `submit-sudoer-request` hands that file to sudoer-cli and does not create the inbound directory and does not write `/etc`.
- **Fail closed.** A missing source, a Termux, Git Bash, or Windows cmd host, a verify mismatch, and a non-empty restore without `--force` stop with an error and a next step.

## Quick Installation

Public source: [https://github.com/cloudgen/PyBackup](https://github.com/cloudgen/PyBackup)

```sh
git clone git@github.com:cloudgen/PyBackup.git
cd PyBackup
python -m pip install --user -e .
py-backup version
```

When the package index lists PyBackup:

```sh
python -m pip install --user PyBackup
```

Pip does not use sudo. Empty arguments do not install or update. This page does not claim the package index already lists PyBackup.

On a terminal, after install:

```text
$ py-backup
Path: <current directory>                                              HH:MM:SS

1. client-side    : this login's folders: pack and restore
3. system-log     : view, clear, and the log folder
4. language       : display language for this menu
5. sudoers        : Grant and drafts
8. self-management: version, about, and pip lifecycle
9. Exit           : leave
╭────────────────────────────────────────────────────────────╮
│ > █                                                        │
╰────────────────────────────────────────────────────────────╯
server-side is not available: this program does not run a host service. Number 2 stays reserved.
  PyBackup 1.0.0  │  main menu  │  Up/Down  •  Enter
```

`1` opens client-side:

```text
11. backup : Pack a named folder into a dated gzip archive under /var/backup/PyBackup
12. restore: Put an archive back onto the hard-disk projects tree
 0. Back   : return to the main menu
```

`5` opens sudoers. The light band under the box says the test commands are typed:

```text
52. submit-sudoer-request : Hand the JSON grant to the approval queue
55. remove-project-sudoers: Remove the local grant draft only
 0. Back                  : return to the main menu
```

`3` opens system-log (`31` view-log, `32` clear-log, `33` log-folder, `0` Back). `4` opens the thirteen languages, `41` English through `53` Ελληνικά, then `0` Back. `8` opens self-management, `82` through `87`, then `0` Back. `9` leaves. The clock on the first row is the local time and moves once a second. The directory on that row is the one you started in.

## Usage

```text
py-backup backup <source-folder>
py-backup restore <archive-or-prefix> [dest] [--force] [--disk] [--ram]
py-backup remove-project-sudoers [path] [--force]
py-backup submit-sudoer-request [file]
py-backup print-sudoers [path]
py-backup print-sudoers-install-script [path]
py-backup generate-sudoer-request [path] [--add] [--update] [--allow-test-local]
py-backup version
py-backup about
py-backup version-check
py-backup self-update
py-backup self-install
py-backup self-uninstall --force
py-backup help
```

`sudoers` is a menu, not a command. `--json` is a flag before the verb. Help lists work commands, then grant and draft setup. Off a terminal, `py-backup` with no command prints help and returns 0.

Environment: `BACKUP_ROOT` (default `/var/backup`), `BACKUP_NOTATION` (default `PyBackup`), `PROJECTS_ROOT`, `RAM_ROOT`, `MAX_DAILY_BACKUPS` (5), `MAX_TOTAL_BACKUPS` (30), `PYBACKUP_LANG`, `GLOBAL_BIN` (default `/usr/local/bin`).

## Examples

```sh
py-backup backup "$HOME/projects/alpha"
py-backup restore alpha
py-backup generate-sudoer-request --allow-test-local
py-backup submit-sudoer-request
py-backup about
```

## Platform Compatibility

| Host | Backup and restore |
|------|--------------------|
| Linux with `tar` | Runs. A deposit you cannot write uses `sudo -n` only after an admin installs the grant. |
| macOS | The same command path. `/var/backup` is not a macOS store unless you set `BACKUP_ROOT`. |
| Termux, Git Bash, Windows Command Prompt | The menu still lists backup and restore. Those verbs stop and do not wrap sudo. |
| WSL | Treated as Linux, not as Windows Command Prompt. |

## Related Projects

- [HelloTui](https://github.com/cloudgen/HelloTui) is the text-menu architecture this program keeps: system log, language, pip self-management, and Exit.

## Contributing

Keep the text-menu rows 3, 4, 8, and 9. Add folder work on rows 1 and 5 and as typed commands. Do not write `/etc` from a normal login. Do not create `/var/sudoer-cli`. Run `sh tests/run.sh` before you call the Python suite done.

## License

MIT. See [LICENSE.md](LICENSE.md). Copyright (c) 2026 cloudgen.

## Last Update

2026-10-23. Package version 1.0.0. Public repository https://github.com/cloudgen/PyBackup. The command is `py-backup`.
