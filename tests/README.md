# Tests — PyBackup

The live command is `py-backup`. The suite under this folder that proves it is Python.

## Run the Python suite

```sh
sh tests/run.sh
```

`tests/run.sh` runs `python3 -m unittest discover -s tests`. Exit **0** when every test passes.

Observed on 2026-10-22: **24** tests, **OK**, about 0.16s, with `PYTHONPATH=src`. Stderr lines that start with `ERROR:` during `test_cli_backup` and `test_unknown_and_force_and_sudoers_word` are the product’s fail-closed messages. Those tests expect them.

## Shell reference runner

```sh
sh tests/run-shell.sh
```

`tests/run-shell.sh` is the runner that used to live at `tests/run.sh` for `src/folder-backup` 1.26.0. It was restored from git so that file can still be exercised. It was **not** executed for the 1.0.0 Python release. Do not cite an older shell PASS count as proof of `py-backup`.

## Layout

| File | Focus |
|------|--------|
| `run.sh` | Python unittest entry |
| `run-shell.sh` | Shell reference entry for `src/folder-backup` |
| `test_pybackup.py` | Menu rows, backup, restore, retention, grant JSON, submit fail-closed |
| `test_cli.sh` and `test_domain_folder_backup.sh` | Shell reference cases. They target `src/folder-backup`. |

## Isolation

Python tests set `BACKUP_ROOT`, `HOME`, and `SUDOER_PUBLIC_ROOT` under a temp directory. They do not create `/var/sudoer-cli`. They do not write `/etc`. A missing backup operand is forced off a terminal so the text menu is not opened.
