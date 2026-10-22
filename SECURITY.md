# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.0 (current Python command `py-backup`) | Yes |
| 1.26.0 (shell record `src/folder-backup`) | Behavioral record; not the `py-backup` command |
| 1.25.0 | Yes |
| 1.24.0 | Yes |
| 1.23.0 | Yes |
| 1.22.0 | Yes |
| 1.21.0 | Yes |
| 1.20.0 | Yes |
| 1.19.0 | Yes |
| 1.18.0 | Yes |
| 1.17.0 | Yes |
| 1.16.5 | Yes |
| 1.16.4 | Yes |
| 1.16.3 | Yes |
| 1.16.2 | Yes |
| 1.15.0 | Yes |
| 1.14.0 | Yes |
| 1.13.0 | Yes |
| 1.12.0 | Yes |
| 1.11.0 | Yes |
| 1.10.0 | Yes |
| 1.9.0 | Yes |
| 1.8.2 | Yes |
| 1.7.0 | Yes |
| 1.6.x | Yes |
| 1.5.x | Best-effort |
| 1.4.x | Best-effort |
| 1.3.x | Best-effort |
| 1.2.x | Best-effort |
| Older releases | Best-effort only |

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
| **C** | **Caution** | Fail closed without working allowlisted sudo for deposit; restore dest **whitelist** (W-ETC-USER `/etc/{{username}}`; never `/etc/passwd`); validate sources and archives. |
| **I** | **Intentional** | Type 0 archive create vs Type 1 deposit/restore-stage copy are separate; `print-sudoers` never writes `/etc`. |
| **A** | **Anti-fragile** | Staging + traps; clear admin install path; hard-disk default restore dest avoids accidental RAM-only recovery assumptions. |
| **O** | **Over-protect** | Narrow command objects only (no `NOPASSWD: ALL`); count and size verification before success. `py-backup` does not download a shell script. On the shell record, a companion digest that does not match aborts that download. |

Full principles: [CIAO](https://github.com/cloudgen/ciao) · [CIAO-Lite](https://github.com/cloudgen/ciao-lite).

This section is **design posture**, not a third-party certification claim.

## Install integrity and trust

Public repository: https://github.com/cloudgen/PyBackup (`git@github.com:cloudgen/PyBackup.git`).

The command `py-backup` installs with `python -m pip`. It does not download a shell script and it does not fetch a companion digest. Production trust for a grant is an executable `py-backup` on `GLOBAL_BIN` (default `/usr/local/bin`). A user-writable `~/.local/bin/py-backup` is test-local only.

The shell file `src/folder-backup` is the 1.26.0 behavioral record. Its historical channel still uses the companion `src/folder-backup.sha256`. That check is not the `py-backup` install path. When `CHECKSUM` is unset, that shell file fetches `${SCRIPT_URL}.sha256`. The table below is that shell record.

| Fact | Honest statement |
|------|------------------|
| **Default path** | Automatic companion verification. No env pin is required for a normal channel install or self-update. |
| **Algorithm** | SHA-256. Human mode shows the companion link, the expected value, and the result. |
| **Match** | Install continues. |
| **Mismatch** | Install aborts. Mismatched bytes are not placed. |
| **Missing sidecar** | Warn and continue. This is not “always verified.” |
| **Optional pin** | `CHECKSUM` is a secondary pin for one run (CI or an out-of-band freeze). It is not listed in `help` or `about`. A pin taken from the same URL is not stronger than the automatic companion. |
| **Trust bound** | Same-channel SHA-256 proves the downloaded file matches the companion. It does not prove a separate signature or a different trust root. |

Operator steps stay in the README. Local `install` copies the file you are running and does not use this check.

## Scope notes

- Elevation for `py-backup` is limited to deposit and restore after an admin installs the grant. The program does not write `/etc`.
- Operators must admin-install sudoers fragments after review (`visudo -c`, mode `0440`).
- **Install trust for `py-backup`:** production is an executable `/usr/local/bin/py-backup` (or `GLOBAL_BIN/py-backup`). Test-local is `~/.local/bin/py-backup`, which this login can rewrite. Generate and print refuse test-local unless `--allow-test-local` is set. `remove-project-sudoers` deletes a local draft only.
- The bullets below are the **shell record** `src/folder-backup` 1.26.0. They are not the `py-backup` install path.
- **Install trust tiers for the shell record:**
  - **Production:** global managed binary (`/usr/local/bin/folder-backup`, typically root-owned). Prefer `sudo folder-backup install` before durable sudoers.  
  - **Test mode only:** local `~/.local/bin/folder-backup` is **user-rewritable**. A local user can change the CLI and stage content after a review; do **not** treat local-only sudoers as production-secure.  
  - `print-sudoers` refuses non-production tiers unless `--allow-test-local` / `ALLOW_TEST_LOCAL_SUDOERS=1`, and embeds **TEST MODE / uninstall soon** warnings.  
  - **`print-sudoers-install-script`** writes a **Type 0 admin handoff script** under `/dev/shm` (or temp) that a sudo-capable account runs for `install` / `uninstall` / `replace` of the **project-sudoers-file** — the CLI never writes `/etc` itself.  
  - **Per-user host paths:** draft `~/.config/folder-backup/sudoers.fragment-<user>` installs to `/etc/sudoers.d/folder-backup-<user>` so multi-user admin installs do not overwrite each other.  
  - Uninstall of the binary does **not** remove `/etc/sudoers.d/folder-backup-<user>` — use `sudo sh <admin-script> uninstall` (or admin `rm`) when leaving test elevation.  
  - **`remove-project-sudoers`** deletes drafts only; when multiple drafts exist it lists them for interactive choice (non-interactive needs an explicit path).  
- Residual: even with OS-tool-only Cmnds, **stage trees are user-writable**; deposit grants write of staged archives into `/var/backup/folder-backup/` only (not a root shell).  
- Related docs: [`README.md`](./README.md), [`LICENSE.md`](./LICENSE.md), `docs/requirements/requirement-three-layer-privilege-model.md`, `reviews/reports/2026-08-09-sudoers-security-folder-backup.md`.
