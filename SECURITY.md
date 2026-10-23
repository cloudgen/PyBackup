# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.0 (`py-backup`) | Yes |

## Reporting a Vulnerability

Please **do not** open a public issue for security-sensitive reports when a private channel is available.

**Maintainer contact (email):** `wongcf22@gmail.com`

- Source of contact: product **author-email** SSOT in [`LICENSE.md`](./LICENSE.md) (Copyright line).  
- Prefer email (or private GitHub security advisories when enabled) for vulnerability details, reproduction steps, and impact.  
- Do not include exploit weaponization guides in public channels.

## Security Design Principles (CIAO)

This project follows **[CIAO](https://github.com/cloudgen/ciao)** / **[CIAO-Lite](https://github.com/cloudgen/ciao-lite)** defensive design. Security-relevant intent:

| Letter | Principle | Security application |
|--------|-----------|----------------------|
| **C** | **Caution** | Fail closed without a working grant for deposit. Restore allows `/etc/<your-login>` and refuses `/etc/passwd`. Sources and archives are checked. |
| **I** | **Intentional** | Creating the archive and copying it into the deposit are separate steps. `print-sudoers` never writes `/etc`. |
| **A** | **Anti-fragile** | The stage is removed after the deposit. The default restore destination is the hard-disk projects tree. |
| **O** | **Over-protect** | The grant is four command objects for `py-backup` only. There is no `NOPASSWD: ALL`. Counts are checked before success. `py-backup` does not download a shell script. |

Full principles: [CIAO](https://github.com/cloudgen/ciao) · [CIAO-Lite](https://github.com/cloudgen/ciao-lite).

This section is **design posture**, not a third-party certification claim.

## Install integrity and trust

Public repository: https://github.com/cloudgen/PyBackup (`git@github.com:cloudgen/PyBackup.git`).

The command `py-backup` installs with `python -m pip`. It does not download a shell script and it does not fetch a companion digest. Production trust for a grant is an executable `py-backup` on `GLOBAL_BIN` (default `/usr/local/bin`). A user-writable `~/.local/bin/py-backup` is test-local only.

| Fact | Honest statement |
|------|------------------|
| **Install** | `python -m pip install --user -e .` from a checkout. `python -m pip install --user PyBackup` when the package index lists it. |
| **No download check** | Pip places the command. This program does not fetch a sidecar digest. |
| **Trust bound** | A grant is production only when `GLOBAL_BIN/py-backup` is executable. A copy under `~/.local/bin` is test-local. |

Operator steps stay in the README.

## Scope notes

- Elevation for `py-backup` is limited to deposit and restore after an admin installs the grant. The program does not write `/etc`.
- Operators must admin-install sudoers fragments after review (`visudo -c`, mode `0440`).
- **Install trust:** production is an executable `/usr/local/bin/py-backup` (or `GLOBAL_BIN/py-backup`). Test-local is `~/.local/bin/py-backup`, which this login can rewrite. Generate and print refuse test-local unless `--allow-test-local` is set. `remove-project-sudoers` deletes a local draft only.
- The draft is `~/.config/PyBackup/sudoer-request-<user>.json`. The fragment an admin installs is `/etc/sudoers.d/PyBackup-<user>`.
- `print-sudoers-install-script` writes an admin script. The command itself does not write `/etc`.
- The stage tree is writable by this login. The deposit grant writes archives under `/var/backup/PyBackup/` only.
- Related docs: [`README.md`](./README.md), [`LICENSE.md`](./LICENSE.md), `docs/requirements/requirement-three-layer-privilege-model.md`.
