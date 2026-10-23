# Tests — PyBackup

The live command is `py-backup`. The suite under this folder that proves it is Python.

## Run the Python suite

```sh
sh tests/run.sh
```

`tests/run.sh` runs `python3 -m unittest discover -s tests`. Exit **0** when every test passes.

Observed on 2026-10-22: **24** tests, **OK**, about 0.16s, with `PYTHONPATH=src`. Stderr lines that start with `ERROR:` during `test_cli_backup` and `test_unknown_and_force_and_sudoers_word` are the product’s fail-closed messages. Those tests expect them.

## Layout

| File | Focus |
|------|--------|
| `run.sh` | Python unittest entry |
| `test_pybackup.py` | Menu rows, backup, restore, retention, grant JSON, submit fail-closed |

## Isolation

Python tests set `BACKUP_ROOT`, `HOME`, and `SUDOER_PUBLIC_ROOT` under a temp directory. They do not create `/var/sudoer-cli`. They do not write `/etc`. A missing backup operand is forced off a terminal so the text menu is not opened.
